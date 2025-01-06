import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import re
from collections import defaultdict
import os
from PIL import Image, ImageDraw, ImageTk
from threading import Thread
from queue import Queue

# Function to create an in-memory book icon
def get_book_icon():
    # Create an image for the icon
    img = Image.new("RGBA", (64, 64), (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(img)

    # Draw book cover
    draw.rectangle([10, 10, 54, 54], fill="blue", outline="black")  # Outer rectangle
    draw.line([12, 12, 12, 52], fill="white", width=2)  # Vertical line for book spine
    draw.line([16, 16, 16, 48], fill="white", width=2)  # Another vertical line for book spine

    # Draw pages
    for i in range(20, 54, 4):
        draw.line([i, 10, i, 54], fill="white", width=1)  # Pages lines

    # Convert to PhotoImage
    return ImageTk.PhotoImage(img)

# Function to parse the WoS text file
def parse_wos_file(filepath, progress_queue):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split articles by PT J to capture all entries
    articles = re.split(r'PT J\n', content)
    data = []

    total_articles = len(articles)

    for i, article in enumerate(articles):
        if not article.strip():
            continue  # Skip empty segments
        
        # Extract and clean the title
        title_match = re.search(r'TI (.*?)\n(?:SO|DE|ID|AB|C1|C3|RP|EM|RI|OI|FU|FX)', article, re.S)
        year_match = re.search(r'PY (\d{4})', article)
        
        # Keywords from DE or ID fields
        keywords_match = re.search(r'DE (.*?)\n', article, re.S)
        id_match = re.search(r'ID (.*?)\n', article, re.S)
        
        keywords = []
        if keywords_match:
            keywords += keywords_match.group(1).replace('\n', ' ').split('; ')
        if id_match:
            keywords += id_match.group(1).replace('\n', ' ').split('; ')
        
        # Remove empty keywords and trailing semicolons
        keywords = [kw.strip(';').strip() for kw in keywords if kw.strip()]
        
        if title_match and year_match:
            # Remove extra spaces from the title and trim trailing text after keywords
            title = title_match.group(1).replace('\n', ' ').strip()
            title = re.sub(r'\s{2,}', ' ', title)  # Replace multiple spaces with a single space
            
            # Clean any potential "keywords-like" artifacts from the title
            title = re.sub(r';.*$', '', title).strip()
            year = year_match.group(1)
            data.append({'Title': title, 'Year': year, 'Keywords': keywords})
        
        # Update progress
        progress_queue.put((i + 1) / total_articles * 100)

    return data

# Function to generate statistics
def generate_statistics(data):
    stats = defaultdict(lambda: defaultdict(int))

    for entry in data:
        year = entry['Year']
        for keyword in entry['Keywords']:
            stats[keyword][year] += 1

    df_stats = pd.DataFrame(stats).fillna(0).astype(int).T
    df_stats['Total'] = df_stats.sum(axis=1)
    df_stats = df_stats.sort_values(by='Total', ascending=False)
    df_stats = df_stats.drop(columns=['Total'])
    df_stats = df_stats.sort_index(axis=1)
    return df_stats

# GUI Application
class WOSParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web of Science Literature Parser")

        # Generate and set window icon directly from memory
        self.icon_image = get_book_icon()
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon_image)

        # Add background
        self.background = Image.new("RGBA", (800, 600), "#F0F8FF")  # Light blue gradient
        self.bg_image = ImageTk.PhotoImage(self.background)
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        self.label = tk.Label(root, text="Select WoS exported .txt files", bg="#F0F8FF", font=("Arial", 14))
        self.label.pack(pady=10)

        self.selected_files = []

        self.file_listbox = tk.Listbox(root, height=10, selectmode=tk.MULTIPLE, font=("Arial", 10))
        self.file_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        self.button_browse = tk.Button(root, text="Browse", command=self.browse_files, relief="groove", borderwidth=2, font=("Arial", 12))
        self.button_browse.pack(pady=5)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.info_text = tk.Text(root, height=10, state=tk.DISABLED, font=("Arial", 10))
        self.info_text.pack(pady=10, fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(root, bg="#F0F8FF")
        self.button_frame.pack(pady=5)

        self.button_process = tk.Button(self.button_frame, text="Process Files", command=self.start_processing, relief="groove", borderwidth=2, font=("Arial", 12))
        self.button_process.grid(row=0, column=0, padx=10)

        self.button_export = tk.Button(self.button_frame, text="Export to Excel", command=self.export_to_excel, relief="groove", borderwidth=2, font=("Arial", 12))
        self.button_export.grid(row=0, column=1, padx=10)

        self.filepaths = []
        self.data = []

    def browse_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        for file in files:
            if file not in self.filepaths:
                self.file_listbox.insert(tk.END, file)
                self.filepaths.append(file)

    def log_info(self, message):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.config(state=tk.DISABLED)
        self.info_text.see(tk.END)

    def start_processing(self):
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

        Thread(target=process_files).start()

    def export_to_excel(self):
        if not self.data:
            messagebox.showwarning("Warning", "No data to export. Please process files first.")
            return

        export_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if export_path:
            try:
                df_articles = pd.DataFrame([{
                    'Title': entry['Title'],
                    'Year': entry['Year'],
                    'Keyword': keyword
                } for entry in self.data for keyword in entry['Keywords']])

                stats_df = generate_statistics(self.data)

                with pd.ExcelWriter(export_path) as writer:
                    df_articles.to_excel(writer, sheet_name='Articles', index=False)
                    stats_df.to_excel(writer, sheet_name='Statistics')

                messagebox.showinfo("Success", "Exported to Excel successfully.")
                self.log_info(f"Exported to: {export_path}")
            except PermissionError:
                messagebox.showerror("Error", "The file is currently in use. Please close it and try again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WOSParserApp(root)
    root.mainloop()
