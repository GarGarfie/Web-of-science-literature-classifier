from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QFileDialog, 
                            QMessageBox, QDialog, QLabel, QListWidget, 
                            QTextEdit, QGroupBox, QGridLayout, QLineEdit)
from PyQt5.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from resources.translations import get_text as _

class MatplotlibCanvas(FigureCanvas):
    """用于在PyQt中嵌入matplotlib图表的画布"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(self.fig)

class CountryMappingDialog(QDialog):
    """国家映射管理对话框"""
    
    def __init__(self, parent, country_analyzer):
        super().__init__(parent)
        self.country_analyzer = country_analyzer
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(_("country_mapping"))
        self.setGeometry(100, 100, 800, 600)
        
        main_layout = QVBoxLayout(self)
        
        # 添加新映射区域
        add_group = QGroupBox(_("add_mapping"))
        add_layout = QGridLayout()
        
        self.original_input = QLineEdit()
        self.translated_input = QLineEdit()
        self.add_button = QPushButton(_("add"))
        self.add_button.clicked.connect(self.add_mapping)
        
        add_layout.addWidget(QLabel(_("original_name")), 0, 0)
        add_layout.addWidget(self.original_input, 0, 1)
        add_layout.addWidget(QLabel(_("translated_name")), 1, 0)
        add_layout.addWidget(self.translated_input, 1, 1)
        add_layout.addWidget(self.add_button, 2, 1)
        
        add_group.setLayout(add_layout)
        main_layout.addWidget(add_group)
        
        # 未识别地址区域
        unknown_group = QGroupBox(_("unknown_addresses"))
        unknown_layout = QVBoxLayout()
        
        self.unknown_addresses = QListWidget()
        self.unknown_addresses.itemClicked.connect(self.select_address)
        
        unknown_layout.addWidget(self.unknown_addresses)
        unknown_group.setLayout(unknown_layout)
        
        # 现有映射区域
        mapping_group = QGroupBox(_("country_mapping"))
        mapping_layout = QVBoxLayout()
        
        self.mapping_table = QTableWidget()
        self.mapping_table.setColumnCount(2)
        self.mapping_table.setHorizontalHeaderLabels([_("original_name"), _("translated_name")])
        
        mapping_layout.addWidget(self.mapping_table)
        mapping_group.setLayout(mapping_layout)
        
        # 将两个区域添加到水平布局
        horiz_layout = QHBoxLayout()
        horiz_layout.addWidget(unknown_group)
        horiz_layout.addWidget(mapping_group)
        
        main_layout.addLayout(horiz_layout)
        
        # 底部按钮
        button_layout = QHBoxLayout()
        
        self.update_button = QPushButton(_("update_analysis"))
        self.update_button.clicked.connect(self.update_analysis)
        
        self.close_button = QPushButton(_("close"))
        self.close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.close_button)
        
        main_layout.addLayout(button_layout)
        
        # 填充数据
        self.populate_unknown_addresses()
        self.populate_mapping_table()
    
    def populate_unknown_addresses(self):
        """填充未识别地址列表"""
        self.unknown_addresses.clear()
        addresses = self.country_analyzer.get_unknown_addresses()
        for address in addresses:
            self.unknown_addresses.addItem(address)
    
    def populate_mapping_table(self):
        """填充映射表"""
        # 获取所有映射
        mappings = sorted(self.country_analyzer.country_mapping.items())
        
        self.mapping_table.setRowCount(len(mappings))
        
        for i, (original, translated) in enumerate(mappings):
            self.mapping_table.setItem(i, 0, QTableWidgetItem(original))
            self.mapping_table.setItem(i, 1, QTableWidgetItem(translated))
        
        self.mapping_table.resizeColumnsToContents()
    
    def select_address(self, item):
        """选择地址时预填充输入"""
        address = item.text()
        # 尝试提取国家名称（通常是最后一部分）
        parts = address.split(',')
        if parts:
            last_part = parts[-1].strip()
            self.original_input.setText(last_part)
    
    def add_mapping(self):
        """添加新的国家映射"""
        original = self.original_input.text().strip()
        translated = self.translated_input.text().strip()
        
        if not original or not translated:
            QMessageBox.warning(self, _("error"), _("input_error"))
            return
        
        # 添加映射
        self.country_analyzer.add_country_mapping(original, translated)
        
        # 清空输入
        self.original_input.clear()
        self.translated_input.clear()
        
        # 更新表格
        self.populate_mapping_table()
        
        QMessageBox.information(self, _("success"), _("mapping_added").format(original, translated))
    
    def update_analysis(self):
        """使用新映射重新分析"""
        # 重新分析数据
        self.country_analyzer.reanalyze_with_new_mapping()
        
        # 更新UI
        self.populate_unknown_addresses()
        
        QMessageBox.information(self, _("success"), _("update_complete"))
        
        # 通知父窗口更新显示
        self.parent().update_with_data(self.country_analyzer.get_countries_data())
    
    def update_translations(self):
        """更新对话框中的所有翻译文本"""
        self.setWindowTitle(_("country_mapping"))
        
        # 更新分组框标题
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if isinstance(item.widget(), QGroupBox):
                if "add" in item.widget().title().lower():
                    item.widget().setTitle(_("add_mapping"))
        
        # 更新标签
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if isinstance(item, QHBoxLayout):
                for j in range(item.count()):
                    widget = item.itemAt(j).widget()
                    if isinstance(widget, QGroupBox):
                        if "unknown" in widget.title().lower():
                            widget.setTitle(_("unknown_addresses"))
                        elif "mapping" in widget.title().lower():
                            widget.setTitle(_("country_mapping"))
        
        # 更新按钮文本
        self.add_button.setText(_("add"))
        self.update_button.setText(_("update_analysis"))
        self.close_button.setText(_("close"))
        
        # 更新表格标题
        self.mapping_table.setHorizontalHeaderLabels([_("original_name"), _("translated_name")])

class CountryTab(QWidget):
    """Web of Science分析工具的国家分析标签页"""
    
    def __init__(self, country_analyzer):
        super().__init__()
        self.country_analyzer = country_analyzer
        self.country_data = {}
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        main_layout = QVBoxLayout(self)
        
        # 控制区域
        controls_layout = QHBoxLayout()
        
        # 国家映射控制
        mapping_box = QGroupBox(_("country_management"))
        mapping_layout = QHBoxLayout()
        self.mapping_button = QPushButton(_("country_mapping"))
        self.mapping_button.clicked.connect(self.open_mapping_dialog)
        
        mapping_layout.addWidget(self.mapping_button)
        mapping_box.setLayout(mapping_layout)
        
        controls_layout.addWidget(mapping_box)
        
        # 导出控制
        export_box = QGroupBox(_("export"))
        export_layout = QHBoxLayout()
        self.export_csv_button = QPushButton(_("export_csv"))
        self.export_csv_button.clicked.connect(self.export_to_csv)
        self.export_graph_button = QPushButton(_("export_graph"))
        self.export_graph_button.clicked.connect(self.export_graph)
        
        export_layout.addWidget(self.export_csv_button)
        export_layout.addWidget(self.export_graph_button)
        export_box.setLayout(export_layout)
        
        controls_layout.addWidget(export_box)
        
        main_layout.addLayout(controls_layout)
        
        # 表格和图表区域
        table_plot_layout = QHBoxLayout()
        
        # 国家表格
        table_layout = QVBoxLayout()
        self.table_label = QLabel(_("country_stats"))
        self.country_table = QTableWidget()
        self.country_table.setEditTriggers(QTableWidget.NoEditTriggers)  # 只读
        
        table_layout.addWidget(self.table_label)
        table_layout.addWidget(self.country_table)
        
        table_plot_layout.addLayout(table_layout)
        
        # 可视化
        plot_layout = QVBoxLayout()
        self.plot_label = QLabel(_("country_trend"))
        self.country_plot = MatplotlibCanvas(width=6, height=4, dpi=100)
        
        plot_layout.addWidget(self.plot_label)
        plot_layout.addWidget(self.country_plot)
        
        table_plot_layout.addLayout(plot_layout)
        
        main_layout.addLayout(table_plot_layout)
        
        # 未识别地址区域
        unknown_layout = QVBoxLayout()
        self.unknown_label = QLabel(_("unknown_addresses"))
        self.unknown_text = QTextEdit()
        self.unknown_text.setReadOnly(True)
        
        unknown_layout.addWidget(self.unknown_label)
        unknown_layout.addWidget(self.unknown_text)
        
        main_layout.addLayout(unknown_layout)
    
    def update_with_data(self, country_data):
        """使用新数据更新标签页
        
        参数:
            country_data (dict): 国家统计数据
        """
        self.country_data = country_data
        
        # 更新国家表格
        self.update_country_table()
        
        # 更新国家图表
        self.update_country_plot()
        
        # 更新未识别地址
        self.update_unknown_addresses()
    
    def update_country_table(self):
        """更新国家统计表"""
        if not self.country_data:
            return
        
        # 获取年份
        years = sorted(set(year for country_data in self.country_data.values() 
                           for year in country_data.keys()))
        
        # 计算每个国家的总数
        totals = {}
        for country, year_data in self.country_data.items():
            totals[country] = sum(year_data.values())
        
        # 按总出版物排序国家
        sorted_countries = sorted(totals.items(), key=lambda x: x[1], reverse=True)
        
        # 设置表格
        self.country_table.setRowCount(len(sorted_countries))
        self.country_table.setColumnCount(len(years) + 2)  # 国家 + 年份 + 总数
        
        # 设置表头
        headers = [_("country")] + years + [_("total")]
        self.country_table.setHorizontalHeaderLabels(headers)
        
        # 填充表格
        for i, (country, total) in enumerate(sorted_countries):
            self.country_table.setItem(i, 0, QTableWidgetItem(country))
            
            year_counts = self.country_data[country]
            col = 1
            for year in years:
                count = year_counts.get(year, 0)
                self.country_table.setItem(i, col, QTableWidgetItem(str(count)))
                col += 1
            
            self.country_table.setItem(i, col, QTableWidgetItem(str(total)))
        
        self.country_table.resizeColumnsToContents()
    
    def update_country_plot(self):
        """更新国家趋势图"""
        if not self.country_data:
            return
        
        self.country_plot.axes.clear()
        
        # 获取总出版物最多的前10个国家
        totals = {}
        for country, year_data in self.country_data.items():
            totals[country] = sum(year_data.values())
        
        top_countries = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 获取年份范围
        years = sorted(set(year for country_data in self.country_data.values() 
                        for year in country_data.keys()))
        
        # 创建堆叠条形图
        bottom = [0] * len(years)
        
        # 颜色循环
        color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        
        # 将每个国家绘制为堆叠条形
        for i, (country, total) in enumerate(top_countries):  # 修改此处，将 _ 改为 total
            year_counts = []
            for year in years:
                count = self.country_data[country].get(year, 0)
                year_counts.append(count)
            
            # 使用循环颜色
            color_idx = i % len(color_cycle)
            
            # 添加国家名称和总数到标签
            label = f"{country} ({totals[country]})"
            
            self.country_plot.axes.bar(
                years, 
                year_counts, 
                label=label, 
                bottom=bottom, 
                color=color_cycle[color_idx]
            )
            
            # 更新底部以进行堆叠
            bottom = [b + c for b, c in zip(bottom, year_counts)]
        
        self.country_plot.axes.set_xlabel(_("year"))
        self.country_plot.axes.set_ylabel(_("publication_count"))
        self.country_plot.axes.set_title(_("country_trend"))
        
        # 旋转X轴标签，防止重叠
        if len(years) > 4:
            plt.setp(self.country_plot.axes.get_xticklabels(), rotation=45, ha='right')
        
        # 设置图例
        self.country_plot.axes.legend(
            loc='upper left', 
            bbox_to_anchor=(1, 1), 
            title=_("country_total_publications")
        )
        
        # 调整布局以适应旋转的标签和图例
        self.country_plot.fig.subplots_adjust(bottom=0.15, right=0.75)
        self.country_plot.draw()
    
    def update_unknown_addresses(self):
        """更新未识别地址文本区域"""
        unknown_addresses = self.country_analyzer.get_unknown_addresses()
        
        if unknown_addresses:
            text = _("The following address does not recognize the country, please add the corresponding relationship in 'Country Mapping Management' / 以下地址无法识别国家，请在'国家映射管理'中添加对应关系 / Следующий адрес не позволяет определить страну, пожалуйста, добавьте соответствующее отношение в «Управление отображением стран».") + "\n\n"
            for address in unknown_addresses:
                text += f"• {address}\n\n"
        else:
            text = _("There are no unrecognized addresses. All addresses have been successfully matched to countries. / 没有未识别的地址。所有地址都已成功匹配到国家。 / Нет нераспознанных адресов. Все адреса были успешно сопоставлены со странами.")
        
        self.unknown_text.setText(text)
    
    def open_mapping_dialog(self):
        """打开国家映射对话框"""
        dialog = CountryMappingDialog(self, self.country_analyzer)
        dialog.exec_()
    
    def export_to_csv(self):
        """将国家数据导出到CSV文件"""
        if not self.country_data:
            QMessageBox.warning(self, _("error"), _("no_data"))
            return
        
        file_path, file_filter = QFileDialog.getSaveFileName(  # 修改此处，将 _ 改为 file_filter
            self, _("export_csv"), "", "CSV " + _("text_files") + " (*.csv)"
        )
        
        if not file_path:
            return
        
        try:
            # 获取年份
            years = sorted(set(year for country_data in self.country_data.values() 
                               for year in country_data.keys()))
            
            # 计算总数并排序国家
            totals = {}
            for country, year_data in self.country_data.items():
                totals[country] = sum(year_data.values())
            
            sorted_countries = sorted(totals.items(), key=lambda x: x[1], reverse=True)
            
            # 创建CSV内容
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                # 写入表头
                header = _("country") + ',' + ','.join(years) + ',' + _("total") + '\n'
                f.write(header)
                
                # 为每个国家写入数据
                for country, count in sorted_countries:  # 修改此处，将 _ 改为 count
                    row = [country]
                    year_data = self.country_data[country]
                    
                    for year in years:
                        count = year_data.get(year, 0)
                        row.append(str(count))
                    
                    row.append(str(totals[country]))
                    f.write(','.join(row) + '\n')
            
            QMessageBox.information(self, _("success"), _("export_success").format(file_path))
        
        except Exception as e:
            QMessageBox.critical(self, _("error"), _("export_error").format(str(e)))
    
    def export_graph(self):
        """将当前图表导出到图像文件"""
        if not self.country_data:
            QMessageBox.warning(self, _("error"), _("no_data"))
            return
        
        file_path, file_filter = QFileDialog.getSaveFileName(  # 修改此处，将 _ 改为 file_filter
            self, _("export_graph"), "", "PNG " + _("text_files") + " (*.png);;PDF " + _("text_files") + " (*.pdf);;SVG " + _("text_files") + " (*.svg)"
        )
        
        if not file_path:
            return
        
        try:
            self.country_plot.fig.savefig(file_path, dpi=300, bbox_inches='tight')
            QMessageBox.information(self, _("success"), _("export_success").format(file_path))
        except Exception as e:
            QMessageBox.critical(self, _("error"), _("export_error").format(str(e)))
    
    def reset(self):
        """将标签页重置为初始状态"""
        self.country_data = {}
        self.country_table.setRowCount(0)
        self.country_table.setColumnCount(0)
        self.country_plot.axes.clear()
        self.country_plot.draw()
        self.unknown_text.clear()
    
    def update_translations(self):
        """更新标签页中的所有翻译文本"""
        # 更新按钮和标签文本
        self.table_label.setText(_("country_stats"))
        self.plot_label.setText(_("country_trend"))
        self.unknown_label.setText(_("unknown_addresses"))
        self.mapping_button.setText(_("country_mapping"))
        self.export_csv_button.setText(_("export_csv"))
        self.export_graph_button.setText(_("export_graph"))
        
        # 更新GroupBox标题
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if isinstance(item, QHBoxLayout):
                for j in range(item.count()):
                    widget = item.itemAt(j).widget()
                    if isinstance(widget, QGroupBox):
                        if "country" in widget.title().lower() or "国家" in widget.title():
                            widget.setTitle(_("country_management"))
                        elif "export" in widget.title().lower() or "导出" in widget.title():
                            widget.setTitle(_("export"))
        
        # 更新表格标题
        if self.country_table.columnCount() > 0:
            current_headers = [self.country_table.horizontalHeaderItem(i).text() 
                            for i in range(self.country_table.columnCount())]
            years = current_headers[1:-1]  # 年份保持不变
            new_headers = [_("country")] + years + [_("total")]
            self.country_table.setHorizontalHeaderLabels(new_headers)
        
        # 更新图表标签
        if hasattr(self, 'country_plot') and self.country_plot.axes:
            self.country_plot.axes.set_xlabel(_("year"))
            self.country_plot.axes.set_ylabel(_("publication_count"))
            self.country_plot.axes.set_title(_("country_trend"))
            
            # 更新图例标题
            legend = self.country_plot.axes.get_legend()
            if legend and legend.get_title():
                legend.set_title(_("country_total_publications"))
            
            self.country_plot.draw()
        
        # 更新未识别地址文本
        self.update_unknown_addresses()