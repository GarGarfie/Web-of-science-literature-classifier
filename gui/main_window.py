from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QFileDialog, QMessageBox,
                            QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
                            QLabel, QListWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from queue import Queue
from modules.file_parser import WoSFileParser
from modules.keyword_analyzer import KeywordAnalyzer
from modules.country_analyzer import CountryAnalyzer
from gui.keyword_tab import KeywordTab
from gui.country_tab import CountryTab
from gui.language_selector import LanguageSelector
from resources.translations import get_text as _

class ParserThread(QThread):
    """用于后台解析文件的线程"""
    progress_updated = pyqtSignal(float)
    completed = pyqtSignal(int)
    
    def __init__(self, parser, filepath):
        super().__init__()
        self.parser = parser
        self.filepath = filepath
        self.progress_queue = Queue()
    
    def run(self):
        try:
            # 解析文件
            record_count = self.parser.parse_file(self.filepath, self.progress_queue)
            
            # 发送完成信号
            self.completed.emit(record_count)
        except Exception as e:
            print(f"解析线程错误: {e}")
            self.completed.emit(0)

class MainWindow(QMainWindow):
    """Web of Science分析工具的主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 创建分析器
        self.file_parser = WoSFileParser()
        self.keyword_analyzer = KeywordAnalyzer()
        self.country_analyzer = CountryAnalyzer()
        
        # 设置UI
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(_("app_title"))
        self.setGeometry(100, 100, 1200, 800)
        
        # 主布局
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # 顶部工具栏 - 添加语言选择器
        toolbar_layout = QHBoxLayout()
        
        # 创建语言选择器
        self.language_selector = LanguageSelector()
        self.language_selector.language_changed.connect(self.on_language_changed)
        
        toolbar_layout.addStretch(1)  # 添加弹性空间，使语言选择器靠右
        toolbar_layout.addWidget(self.language_selector)
        
        main_layout.addLayout(toolbar_layout)
        
        # 文件选择区域
        file_layout = QVBoxLayout()
        
        file_header = QHBoxLayout()
        self.file_label = QLabel(_("file_select"))
        self.browse_button = QPushButton(_("browse"))
        self.browse_button.clicked.connect(self.open_file_dialog)
        
        file_header.addWidget(self.file_label)
        file_header.addWidget(self.browse_button)
        file_layout.addLayout(file_header)
        
        # 文件列表
        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(100)
        file_layout.addWidget(self.file_list)
        
        main_layout.addLayout(file_layout)
        
        # 标签页
        self.tabs = QTabWidget()
        
        # 创建不同分析的标签页
        self.keyword_tab = KeywordTab(self.keyword_analyzer)
        self.country_tab = CountryTab(self.country_analyzer)
        
        self.tabs.addTab(self.keyword_tab, _("tab_keywords"))
        self.tabs.addTab(self.country_tab, _("tab_countries"))
        
        main_layout.addWidget(self.tabs)
        
        # 底部按钮
        button_layout = QHBoxLayout()
        
        self.reset_button = QPushButton(_("reset_all"))
        self.reset_button.clicked.connect(self.reset_data)
        
        self.debug_button = QPushButton(_("debug_info"))
        self.debug_button.clicked.connect(self.show_debug_info)
        
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.debug_button)
        
        main_layout.addLayout(button_layout)
        
        self.setCentralWidget(central_widget)
    
    def on_language_changed(self, language_code):
        """当语言改变时更新UI文本"""
        # 更新窗口标题
        self.setWindowTitle(_("app_title"))
        
        # 更新主窗口文本
        self.file_label.setText(_("file_select"))
        self.browse_button.setText(_("browse"))
        self.reset_button.setText(_("reset_all"))
        self.debug_button.setText(_("debug_info"))
        
        # 更新标签页标题
        self.tabs.setTabText(0, _("tab_keywords"))
        self.tabs.setTabText(1, _("tab_countries"))
        
        # 更新各标签页内容
        self.keyword_tab.update_translations()
        self.country_tab.update_translations()
    
    def open_file_dialog(self):
        """打开文件选择对话框选择文件"""
        # 使用file_filter代替_作为变量名，避免与翻译函数冲突
        file_path, file_filter = QFileDialog.getOpenFileName(
            self, _("open_wos_files"), "", _("text_files") + " (*.txt)"
        )
        
        if not file_path:
            return  # 用户取消选择，直接返回
        
        # 清空文件列表并添加新文件
        self.file_list.clear()
        
        # 获取文件名（不含路径）并添加到列表
        file_name = file_path.split('/')[-1].split('\\')[-1]  # 处理不同操作系统路径分隔符
        self.file_list.addItem(file_name)
        
        # 处理文件
        self.process_file(file_path)
    
    def process_file(self, file_path):
        """处理单个文件"""
        # 使用线程解析文件
        self.parser_thread = ParserThread(self.file_parser, file_path)
        self.parser_thread.completed.connect(self.file_parsing_completed)
        self.parser_thread.start()
    
    def file_parsing_completed(self, record_count):
        # 获取所有记录
        records = self.file_parser.get_records()
        
        # 关键词分析
        keyword_stats = self.keyword_analyzer.process_keywords(records)
        self.keyword_tab.update_with_data(keyword_stats, records)
        
        # 国家分析
        country_stats = self.country_analyzer.analyze_countries(records)
        self.country_tab.update_with_data(country_stats)
        
        QMessageBox.information(self, _("import_complete"), 
                               _("import_success").format(record_count))
    
    def reset_data(self):
        # 重置所有数据
        self.file_parser.reset()
        self.keyword_analyzer.reset()
        self.country_analyzer.reset()
        self.keyword_tab.reset()
        self.country_tab.reset()
        self.file_list.clear()
        self.file_label.setText(_("file_select"))
        QMessageBox.information(self, _("reset_complete"), _("reset_msg"))
    
    def show_debug_info(self):
        # 显示所有组件的调试信息
        debug_info = []
        debug_info.extend(self.file_parser.get_debug_info())
        debug_info.extend(self.keyword_analyzer.get_debug_info())
        debug_info.extend(self.country_analyzer.get_debug_info())
        
        if not debug_info:
            debug_info = [_("no_data")]
        
        # 显示调试对话框
        msg = QMessageBox()
        msg.setWindowTitle(_("debug_info"))
        msg.setText("\n".join(debug_info))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()