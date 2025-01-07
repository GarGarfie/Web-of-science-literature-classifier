import sys
import subprocess
import importlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import defaultdict
from threading import Thread
from queue import Queue
import re
import os

# 需要的包列表
required_packages = [
    ('pandas', 'pandas'),
    ('Pillow', 'PIL'),
    ('openpyxl', 'openpyxl'),
    ('inflect', 'inflect'),
    ('fuzzywuzzy', 'fuzzywuzzy'),  # Added for fuzzy matching
    ('python-Levenshtein', 'Levenshtein'),  # Optional but recommended for speed
]

def install_packages(packages):
    """
    安装缺失的包。
    
    Args:
        packages (list): 包含包名称的列表。
    """
    for package, module_name in packages:
        try:
            importlib.import_module(module_name)
        except ImportError:
            print(f"Installing missing package: {package}")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# 安装缺失的包
install_packages(required_packages)

# 现在进行静态导入
import pandas as pd
from PIL import Image, ImageDraw, ImageTk
import openpyxl
import inflect
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# 初始化 inflect 引擎
p = inflect.engine()

def get_book_icon():
    """
    使用 PIL 创建一个内存中的书籍图标。

    Returns:
        ImageTk.PhotoImage: 生成的书籍图标。
    """
    # 创建透明图像
    img = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 绘制书籍封面
    draw.rectangle([10, 10, 54, 54], fill="blue", outline="black")
    draw.line([12, 12, 12, 52], fill="white", width=2)
    draw.line([16, 16, 16, 48], fill="white", width=2)

    # 绘制页面
    for i in range(20, 54, 4):
        draw.line([i, 10, i, 54], fill="white", width=1)

    # 转换为 PhotoImage
    return ImageTk.PhotoImage(img)

def singularize_keyword(keyword):
    """
    将关键词短语的最后一个词转换为单数形式。
    同时，用空格替换连字符以确保格式一致。

    Args:
        keyword (str): 要单数化的关键词短语。

    Returns:
        str: 单数化后的关键词短语。
    """
    # 替换连字符为空格
    keyword = keyword.replace('-', ' ')

    words = keyword.split()
    if not words:
        return keyword
    # 仅将最后一个词单数化
    last_word = words[-1]
    singular_last_word = p.singular_noun(last_word)
    if singular_last_word:
        words[-1] = singular_last_word
    return ' '.join(words)

def parse_wos_file(filepath, progress_queue):
    """
    解析 WoS 导出的文本文件以提取标题、年份和关键词。

    Args:
        filepath (str): 文本文件的路径。
        progress_queue (Queue): 更新进度的队列。

    Returns:
        list: 包含 'Title', 'Year' 和 'Keywords' 的字典列表。
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # 通过 'PT J' 分割文章以捕获所有条目
    articles = re.split(r'PT J\n', content)
    data = []

    total_articles = len(articles)

    for i, article in enumerate(articles):
        if not article.strip():
            continue  # 跳过空段

        # 提取并清理标题
        title_match = re.search(r'TI (.*?)\n(?:SO|DE|ID|AB|C1|C3|RP|EM|RI|OI|FU|FX)', article, re.S)
        year_match = re.search(r'PY (\d{4})', article)

        # 从 DE 或 ID 字段提取关键词
        keywords_match = re.search(r'DE (.*?)\n', article, re.S)
        id_match = re.search(r'ID (.*?)\n', article, re.S)

        keywords = []
        if keywords_match:
            # 分割关键词，转换为小写，替换连字符，并单数化
            keywords += [
                singularize_keyword(kw.strip(';').strip().lower())
                for kw in keywords_match.group(1).replace('\n', ' ').split('; ')
                if kw.strip()
            ]
        if id_match:
            # 分割 ID 关键词，转换为小写，替换连字符，并单数化
            keywords += [
                singularize_keyword(kw.strip(';').strip().lower())
                for kw in id_match.group(1).replace('\n', ' ').split('; ')
                if kw.strip()
            ]

        if title_match and year_match:
            # 去除标题中的多余空格，并修剪关键词后的尾随文本
            title = title_match.group(1).replace('\n', ' ').strip()
            title = re.sub(r'\s{2,}', ' ', title)  # 将多个空格替换为一个空格

            # 清理标题中的潜在“类似关键词”的工件
            title = re.sub(r';.*$', '', title).strip()
            year = year_match.group(1)
            data.append({'Title': title, 'Year': year, 'Keywords': keywords})

        # 更新进度
        progress_queue.put((i + 1) / total_articles * 100)

    return data

def generate_statistics(data):
    """
    生成每年的关键词统计。

    Args:
        data (list): 包含 'Title', 'Year' 和 'Keywords' 的字典列表。

    Returns:
        pandas.DataFrame: 以关键词为行，年份为列的 DataFrame。
    """
    stats = defaultdict(lambda: defaultdict(int))

    for entry in data:
        year = entry['Year']
        for keyword in entry['Keywords']:
            stats[keyword][year] += 1  # 关键词已转换为小写并单数化

    df_stats = pd.DataFrame(stats).fillna(0).astype(int).T
    df_stats['Total'] = df_stats.sum(axis=1)
    df_stats = df_stats.sort_values(by='Total', ascending=False)
    df_stats = df_stats.drop(columns=['Total'])
    df_stats = df_stats.sort_index(axis=1)
    return df_stats

def group_similar_keywords(df_stats, threshold=80):
    """
    将相似的关键词分组。

    Args:
        df_stats (pd.DataFrame): 以关键词为行，年份为列的 DataFrame。
        threshold (int): 相似度阈值（0-100）。

    Returns:
        list: 每个组是一个包含相似关键词的列表。
    """
    keywords = list(df_stats.index)
    groups = []
    used = set()

    for keyword in keywords:
        if keyword in used:
            continue
        # 找出与当前关键词相似且未使用的关键词
        similar = process.extract(keyword, keywords, scorer=fuzz.token_sort_ratio)
        similar_keywords = [k for k, score in similar if score >= threshold and k not in used]
        if similar_keywords:
            groups.append(similar_keywords)
            used.update(similar_keywords)

    return groups

class WOSParserApp:
    """
    用于解析 Web of Science (WoS) 导出的文本文件的 GUI 应用程序。
    """

    def __init__(self, root):
        """
        初始化 GUI 组件。

        Args:
            root (tk.Tk): 根窗口。
        """
        self.root = root
        self.root.title("Web of Science Literature Parser")
        self.root.configure(bg="#F0F8FF")  # 设置背景颜色

        # 直接从内存生成并设置窗口图标
        self.icon_image = get_book_icon()
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon_image)

        # 文件选择标签
        self.label = tk.Label(root, text="Select WoS exported .txt files", bg="#F0F8FF", font=("Arial", 14))
        self.label.pack(pady=10)

        self.selected_files = []

        # 显示选择文件的列表框
        self.file_listbox = tk.Listbox(root, height=10, selectmode=tk.MULTIPLE, font=("Arial", 10))
        self.file_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        # 浏览按钮
        self.button_browse = tk.Button(root, text="Browse", command=self.browse_files, relief="groove", borderwidth=2, font=("Arial", 12))
        self.button_browse.pack(pady=5)

        # 进度条
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        # 显示信息的文本框
        self.info_text = tk.Text(root, height=10, state=tk.DISABLED, font=("Arial", 10), bg="#F0F8FF")
        self.info_text.pack(pady=10, fill=tk.BOTH, expand=True)

        # 处理和导出按钮的框架
        self.button_frame = tk.Frame(root, bg="#F0F8FF")
        self.button_frame.pack(pady=5)

        # 处理文件按钮
        self.button_process = tk.Button(
            self.button_frame, text="Process Files", command=self.start_processing,
            relief="groove", borderwidth=2, font=("Arial", 12)
        )
        self.button_process.grid(row=0, column=0, padx=10)

        # 导出到 Excel 按钮
        self.button_export = tk.Button(
            self.button_frame, text="Export to Excel", command=self.export_to_excel,
            relief="groove", borderwidth=2, font=("Arial", 12)
        )
        self.button_export.grid(row=0, column=1, padx=10)

        self.filepaths = []
        self.data = []
        self.df_stats = None  # To store statistics DataFrame

    def browse_files(self):
        """
        打开文件对话框以选择多个 .txt 文件并将其添加到列表框中。
        """
        files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        for file in files:
            if file not in self.filepaths:
                self.file_listbox.insert(tk.END, file)
                self.filepaths.append(file)

    def log_info(self, message):
        """
        将消息记录到 info_text 小部件中。

        Args:
            message (str): 要记录的消息。
        """
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.config(state=tk.DISABLED)
        self.info_text.see(tk.END)

    def start_processing(self):
        """
        在单独的线程中开始处理选定的文件。
        """
        if not self.filepaths:
            messagebox.showwarning("Warning", "Please select files to process.")
            return

        self.progress["value"] = 0
        self.data = []
        self.log_info("Starting processing...")

        progress_queue = Queue()

        def process_files():
            total_files = len(self.filepaths)

            for idx, filepath in enumerate(self.filepaths):
                self.log_info(f"Processing file {idx + 1}/{total_files}: {filepath}")

                try:
                    data = parse_wos_file(filepath, progress_queue)
                    self.data.extend(data)
                    self.log_info(f"Successfully processed: {filepath}")
                except Exception as e:
                    self.log_info(f"Failed to process {filepath}: {e}")

                self.progress["value"] = (idx + 1) / total_files * 100

            self.log_info("Processing complete. Ready to export.")
            self.df_stats = generate_statistics(self.data)  # Generate statistics after processing

        Thread(target=process_files).start()

    def export_to_excel(self):
        """
        将处理后的数据导出到带有调整列宽的 Excel 文件中。
        """
        if not self.data:
            messagebox.showwarning("Warning", "No data to export. Please process files first.")
            return

        export_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if export_path:
            try:
                # 创建文章的 DataFrame
                df_articles = pd.DataFrame([
                    {
                        'Title': entry['Title'],
                        'Year': entry['Year'],
                        'Keyword': keyword
                    }
                    for entry in self.data for keyword in entry['Keywords']
                ])

                # 生成统计数据的 DataFrame
                if self.df_stats is None:
                    self.df_stats = generate_statistics(self.data)

                # 生成相似关键词分组
                groups = group_similar_keywords(self.df_stats, threshold=80)  # You can adjust the threshold

                # Create a DataFrame for grouped keywords
                grouped_data = []
                for group in groups:
                    # Aggregate yearly data
                    aggregated = defaultdict(int)
                    for keyword in group:
                        for year, count in self.df_stats.loc[keyword].items():
                            aggregated[year] += count
                    # Sort years
                    sorted_years = sorted(aggregated.keys())
                    grouped_entry = {f"Keyword {i+1}": kw for i, kw in enumerate(group)}
                    for year in sorted_years:
                        grouped_entry[year] = aggregated[year]
                    grouped_data.append(grouped_entry)

                # Determine all possible year columns
                all_years = sorted({year for group in grouped_data for year in group.keys() if year.isdigit()}, key=int)
                # Determine the maximum number of keywords in a group
                max_keywords = max(len(group) for group in groups) if groups else 0

                # Define column order: Keyword 1, Keyword 2, ..., Year1, Year2, ...
                columns = [f"Keyword {i+1}" for i in range(max_keywords)] + all_years

                df_grouped = pd.DataFrame(grouped_data, columns=columns).fillna('')

                # 将 DataFrame 写入 Excel
                with pd.ExcelWriter(export_path, engine='openpyxl') as writer:
                    df_articles.to_excel(writer, sheet_name='Articles', index=False)
                    self.df_stats.to_excel(writer, sheet_name='Statistics')
                    df_grouped.to_excel(writer, sheet_name='Grouped Keywords', index=False)

                # 加载工作簿以调整列宽
                wb = openpyxl.load_workbook(export_path)
                for sheet_name in wb.sheetnames:
                    ws = wb[sheet_name]
                    for column in ws.columns:
                        max_length = 0
                        column_letter = column[0].column_letter  # 获取列名

                        for cell in column:
                            try:
                                cell_value = str(cell.value)
                                if len(cell_value) > max_length:
                                    max_length = len(cell_value)
                            except:
                                pass

                        # 设置带有一些填充的列宽
                        adjusted_width = (max_length + 2)
                        ws.column_dimensions[column_letter].width = adjusted_width

                # 保存调整列宽后的工作簿
                wb.save(export_path)

                messagebox.showinfo("Success", "Exported to Excel successfully.")
                self.log_info(f"Exported to: {export_path}")
            except PermissionError:
                messagebox.showerror("Error", "The file is currently in use. Please close it and try again.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while exporting: {e}")

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    app = WOSParserApp(root)
    root.mainloop()
