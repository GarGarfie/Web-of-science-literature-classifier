from PyQt5.QtWidgets import QComboBox, QWidget, QHBoxLayout, QLabel, QApplication, QMainWindow, QPushButton, QGroupBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from resources.translations import set_language, get_text as _
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

class LanguageSelector(QWidget):
    """语言选择器组件"""
    
    language_changed = pyqtSignal(str)  # 当语言改变时发出信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        # 初始化字体设置
        self.setup_fonts_for_language('en')
    
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(_("language"))
        
        self.combo = QComboBox()
        self.combo.addItem("English", "en")
        self.combo.addItem("中文", "zh")
        self.combo.addItem("Русский", "ru")
        
        self.combo.currentIndexChanged.connect(self.on_language_changed)
        
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
    
    def on_language_changed(self, index):
        """当选择的语言改变时处理"""
        language_code = self.combo.itemData(index)
        set_language(language_code)
        
        # 为当前语言设置合适的字体
        self.setup_fonts_for_language(language_code)
        
        # 发出语言变化信号
        self.language_changed.emit(language_code)
        
        # 强制处理待处理事件，确保信号被处理
        QApplication.processEvents()
        
        # 查找主窗口并进行深度更新
        main_window = self.find_main_window()
        if main_window:
            # 更新标签页
            self.update_all_tab_translations(main_window)
            
            # 更新所有导出相关按钮和组框
            self.update_export_elements(main_window)
            
            # 强制重绘主窗口
            main_window.update()
    
    def setup_fonts_for_language(self, language_code):
        """为指定语言设置合适的字体"""
        app = QApplication.instance()
        
        # 为UI元素设置Times New Roman
        ui_font = QFont("Times New Roman", 10)
        app.setFont(ui_font)
        
        # 为matplotlib设置支持多语言的字体
        if language_code == 'zh':
            # 中文使用黑体字体
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['font.family'] = 'sans-serif'
        elif language_code == 'ru':
            # 俄语使用支持西里尔字母的字体
            plt.rcParams['font.family'] = 'Times New Roman'
        else:  # 'en' and others
            # 英文使用Times New Roman
            plt.rcParams['font.family'] = 'Times New Roman'
        
        # 确保显示数学符号和负号
        plt.rcParams['axes.unicode_minus'] = False
    
    def get_available_fonts(self):
        """获取系统中可用的字体列表"""
        return [f.name.lower() for f in fm.fontManager.ttflist]
    
    def find_main_window(self):
        """查找主窗口实例"""
        # 获取所有顶级窗口
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                return widget
        return None
    
    def update_all_tab_translations(self, parent_widget):
        """递归更新所有有update_translations方法的子部件"""
        # 直接更新有update_translations方法的部件
        for widget in parent_widget.findChildren(QWidget):
            if hasattr(widget, 'update_translations'):
                widget.update_translations()
    
    def update_export_elements(self, parent_widget):
        """显式更新所有导出相关的UI元素"""
        # 更新所有可能与导出相关的按钮
        for button in parent_widget.findChildren(QPushButton):
            # 检查按钮文本是否与导出相关
            text = button.text().lower()
            if ("export" in text or "导出" in text or "экспорт" in text):
                # 根据按钮文本内容确定其功能并更新
                if "excel" in text:
                    button.setText(_("export_excel"))
                elif "graph" in text or "图表" in text or "график" in text:
                    button.setText(_("export_graph"))
                elif "csv" in text:
                    button.setText(_("export_csv"))
        
        # 更新所有导出相关的组框
        for groupbox in parent_widget.findChildren(QGroupBox):
            title = groupbox.title().lower()
            if "export" in title or "导出" in title or "экспорт" in title:
                groupbox.setTitle(_("export"))
    
    def get_current_language(self):
        """获取当前选择的语言代码"""
        return self.combo.itemData(self.combo.currentIndex())