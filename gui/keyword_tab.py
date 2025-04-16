from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QFileDialog, 
                            QMessageBox, QGroupBox, QLabel, QSpinBox)
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

class KeywordTab(QWidget):
    """Web of Science分析工具的关键词分析标签页"""
    
    def __init__(self, keyword_analyzer):
        super().__init__()
        self.keyword_analyzer = keyword_analyzer
        self.keyword_stats = {}
        self.records = []
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        main_layout = QVBoxLayout(self)
        
        # 控制区域
        controls_layout = QHBoxLayout()
        
        # 分组控制
        grouping_box = QGroupBox(_("similar_groups"))
        grouping_layout = QHBoxLayout()
        self.similarity_label = QLabel(_("similarity_threshold"))
        self.similarity_spinner = QSpinBox()
        self.similarity_spinner.setRange(50, 100)
        self.similarity_spinner.setValue(80)
        self.group_button = QPushButton(_("group_keywords"))
        self.group_button.clicked.connect(self.group_keywords)
        
        grouping_layout.addWidget(self.similarity_label)
        grouping_layout.addWidget(self.similarity_spinner)
        grouping_layout.addWidget(self.group_button)
        grouping_box.setLayout(grouping_layout)
        
        controls_layout.addWidget(grouping_box)
        
        # 导出控制
        export_box = QGroupBox(_("export"))
        export_layout = QHBoxLayout()
        self.export_excel_button = QPushButton(_("export_excel"))
        self.export_excel_button.clicked.connect(self.export_to_excel)
        self.export_graph_button = QPushButton(_("export_graph"))
        self.export_graph_button.clicked.connect(self.export_graph)
        
        export_layout.addWidget(self.export_excel_button)
        export_layout.addWidget(self.export_graph_button)
        export_box.setLayout(export_layout)
        
        controls_layout.addWidget(export_box)
        
        main_layout.addLayout(controls_layout)
        
        # 表格和图表区域
        table_plot_layout = QHBoxLayout()
        
        # 关键词表格
        table_layout = QVBoxLayout()
        self.table_label = QLabel(_("keyword_stats"))
        self.keyword_table = QTableWidget()
        self.keyword_table.setEditTriggers(QTableWidget.NoEditTriggers)  # 只读
        
        table_layout.addWidget(self.table_label)
        table_layout.addWidget(self.keyword_table)
        
        table_plot_layout.addLayout(table_layout)
        
        # 可视化
        plot_layout = QVBoxLayout()
        self.plot_label = QLabel(_("keyword_trend"))
        self.keyword_plot = MatplotlibCanvas(width=6, height=4, dpi=100)
        
        plot_layout.addWidget(self.plot_label)
        plot_layout.addWidget(self.keyword_plot)
        
        table_plot_layout.addLayout(plot_layout)
        
        main_layout.addLayout(table_plot_layout)
        
        # 分组关键词区域
        grouped_layout = QVBoxLayout()
        self.grouped_label = QLabel(_("similar_groups"))
        self.grouped_table = QTableWidget()
        self.grouped_table.setEditTriggers(QTableWidget.NoEditTriggers)  # 只读
        
        grouped_layout.addWidget(self.grouped_label)
        grouped_layout.addWidget(self.grouped_table)
        
        main_layout.addLayout(grouped_layout)
    
    def update_with_data(self, keyword_stats, records):
        """使用新数据更新标签页
        
        参数:
            keyword_stats (dict): 关键词统计数据
            records (list): 记录字典列表
        """
        self.keyword_stats = keyword_stats
        self.records = records
        
        # 更新关键词统计表
        self.update_keyword_table()
        
        # 更新关键词趋势图
        self.update_keyword_plot()
    
    def update_keyword_table(self):
        """更新关键词统计表"""
        if not self.keyword_stats:
            return
            
        # 获取年份
        years = sorted(set(year for keyword_data in self.keyword_stats.values() 
                          for year in keyword_data.keys()))
        
        # 计算每个关键词的总数
        totals = {}
        for keyword, year_data in self.keyword_stats.items():
            totals[keyword] = sum(year_data.values())
        
        # 按总出现次数排序关键词
        sorted_keywords = sorted(totals.items(), key=lambda x: x[1], reverse=True)
        
        # 设置表格
        self.keyword_table.setRowCount(len(sorted_keywords))
        self.keyword_table.setColumnCount(len(years) + 2)  # 关键词 + 年份 + 总数
        
        # 设置表头
        headers = [_("keyword")] + years + [_("total")]
        self.keyword_table.setHorizontalHeaderLabels(headers)
        
        # 填充表格
        for i, (keyword, total) in enumerate(sorted_keywords):
            self.keyword_table.setItem(i, 0, QTableWidgetItem(keyword))
            
            year_counts = self.keyword_stats[keyword]
            col = 1
            for year in years:
                count = year_counts.get(year, 0)
                self.keyword_table.setItem(i, col, QTableWidgetItem(str(count)))
                col += 1
            
            self.keyword_table.setItem(i, col, QTableWidgetItem(str(total)))
        
        self.keyword_table.resizeColumnsToContents()
    
    def update_keyword_plot(self):
        """更新关键词趋势图"""
        if not self.keyword_stats:
            return
            
        self.keyword_plot.axes.clear()
        
        # 获取总数最多的前10个关键词
        totals = {}
        for keyword, year_data in self.keyword_stats.items():
            totals[keyword] = sum(year_data.values())
        
        top_keywords = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 获取年份范围
        years = sorted(set(year for keyword_data in self.keyword_stats.values() 
                        for year in keyword_data.keys()))
        
        # 为每个热门关键词绘制趋势
        for keyword, count in top_keywords:  # 修改此处，将 _ 改为 count
            year_counts = []
            for year in years:
                count = self.keyword_stats[keyword].get(year, 0)
                year_counts.append(count)
            
            self.keyword_plot.axes.plot(years, year_counts, marker='o', label=keyword)
        
        # 设置轴标签和标题
        self.keyword_plot.axes.set_xlabel(_("year"))
        self.keyword_plot.axes.set_ylabel(_("count"))
        self.keyword_plot.axes.set_title(_("keyword_trend"))
        
        # 旋转X轴标签，防止重叠
        if len(years) > 4:
            plt.setp(self.keyword_plot.axes.get_xticklabels(), rotation=45, ha='right')
        
        # 调整图例位置并避免遮挡
        self.keyword_plot.axes.legend(loc='upper left', bbox_to_anchor=(1, 1))
        
        # 调整布局以适应旋转的标签和图例
        self.keyword_plot.fig.subplots_adjust(bottom=0.15, right=0.75)
        self.keyword_plot.draw()
    
    def group_keywords(self):
        """基于相似度阈值对关键词进行分组"""
        if not self.keyword_stats:
            QMessageBox.warning(self, _("error"), _("no_data"))
            return
        
        threshold = self.similarity_spinner.value()
        groups = self.keyword_analyzer.group_similar_keywords(self.keyword_stats, threshold)
        
        # 更新分组关键词表格
        self.update_grouped_table(groups)
    
    def update_grouped_table(self, groups):
        """更新分组关键词表格
        
        参数:
            groups (list): 关键词组列表
        """
        if not groups:
            self.grouped_table.setRowCount(0)
            self.grouped_table.setColumnCount(0)
            return
        
        # 确定任何组中的最大关键词数
        max_keywords = max(len(group) for group in groups)
        
        # 设置表格
        self.grouped_table.setRowCount(len(groups))
        self.grouped_table.setColumnCount(max_keywords + 1)  # +1用于总计列
        
        # 设置表头
        headers = [f'{_("keyword")} {i+1}' for i in range(max_keywords)] + [_("total")]
        self.grouped_table.setHorizontalHeaderLabels(headers)
        
        # 填充表格
        for row, group in enumerate(groups):
            total = 0
            for col, keyword in enumerate(group):
                self.grouped_table.setItem(row, col, QTableWidgetItem(keyword))
                
                # 计算此关键词的总计数
                keyword_total = sum(self.keyword_stats.get(keyword, {}).values())
                total += keyword_total
            
            # 添加总计数列
            self.grouped_table.setItem(row, max_keywords, QTableWidgetItem(str(total)))
        
        self.grouped_table.resizeColumnsToContents()
    
    def export_to_excel(self):
        """将关键词数据导出到Excel文件"""
        if not self.keyword_stats:
            QMessageBox.warning(self, _("error"), _("no_data"))
            return
        
        file_path, file_filter = QFileDialog.getSaveFileName(  # 修改此处，将 _ 改为 file_filter
            self, _("save_file"), "", "Excel " + _("text_files") + " (*.xlsx)"
        )
        
        if not file_path:
            return
        
        try:
            # 创建关键词统计的DataFrame
            years = sorted(set(year for keyword_data in self.keyword_stats.values() 
                              for year in keyword_data.keys()))
            
            # 用零初始化DataFrame
            df_stats = pd.DataFrame(index=self.keyword_stats.keys(), columns=years)
            df_stats = df_stats.fillna(0)
            
            # 填充实际值
            for keyword, year_data in self.keyword_stats.items():
                for year, count in year_data.items():
                    df_stats.at[keyword, year] = count
            
            # 按总出现次数排序
            df_stats[_("total")] = df_stats.sum(axis=1)
            df_stats = df_stats.sort_values(by=_("total"), ascending=False)
            
            # 创建带有关键词的文章DataFrame
            articles_data = []
            for record in self.records:
                if 'Keywords' in record and record['Keywords']:
                    title = record.get('TI', '') or record.get('Title', '')
                    year = record.get('PY', '') or record.get('Year', '')
                    
                    for keyword in record['Keywords']:
                        articles_data.append({
                            _("title"): title,
                            _("year"): year,
                            _("keyword"): keyword
                        })
            
            df_articles = pd.DataFrame(articles_data)
            
            # 获取分组关键词
            threshold = self.similarity_spinner.value()
            groups = self.keyword_analyzer.group_similar_keywords(self.keyword_stats, threshold)
            
            # 创建分组关键词DataFrame
            grouped_data = []
            max_keywords = max(len(group) for group in groups) if groups else 0
            
            for group in groups:
                # 为每个组创建新行
                group_row = {}
                
                # 添加每个关键词
                for i, keyword in enumerate(group):
                    group_row[f'{_("keyword")} {i+1}'] = keyword
                
                # 添加年份计数（汇总组中所有关键词）
                for year in years:
                    group_row[year] = sum(self.keyword_stats.get(kw, {}).get(year, 0) for kw in group)
                
                grouped_data.append(group_row)
            
            if grouped_data:
                columns = [f'{_("keyword")} {i+1}' for i in range(max_keywords)] + years
                df_grouped = pd.DataFrame(grouped_data, columns=columns)
            else:
                df_grouped = pd.DataFrame()
            
            # 写入Excel文件
            with pd.ExcelWriter(file_path) as writer:
                df_stats.to_excel(writer, sheet_name=_("keyword_stats"))
                df_articles.to_excel(writer, sheet_name=_("articles"), index=False)
                if not df_grouped.empty:
                    df_grouped.to_excel(writer, sheet_name=_("similar_groups"), index=False)
            
            QMessageBox.information(self, _("success"), _("export_success").format(file_path))
        
        except Exception as e:
            QMessageBox.critical(self, _("error"), _("export_error").format(str(e)))
    
    def export_graph(self):
        """将当前图表导出到图像文件"""
        if not self.keyword_stats:
            QMessageBox.warning(self, _("error"), _("no_data"))
            return
        
        file_path, file_filter = QFileDialog.getSaveFileName(  # 修改此处，将 _ 改为 file_filter
            self, _("export_graph"), "", "PNG " + _("text_files") + " (*.png);;PDF " + _("text_files") + " (*.pdf);;SVG " + _("text_files") + " (*.svg)"
        )
        
        if not file_path:
            return
        
        try:
            self.keyword_plot.fig.savefig(file_path, dpi=300, bbox_inches='tight')
            QMessageBox.information(self, _("success"), _("export_success").format(file_path))
        except Exception as e:
            QMessageBox.critical(self, _("error"), _("export_error").format(str(e)))
    
    def reset(self):
        """将标签页重置为初始状态"""
        self.keyword_stats = {}
        self.records = []
        self.keyword_table.setRowCount(0)
        self.keyword_table.setColumnCount(0)
        self.grouped_table.setRowCount(0)
        self.grouped_table.setColumnCount(0)
        self.keyword_plot.axes.clear()
        self.keyword_plot.draw()
        
    def update_translations(self):
        """更新标签页中的所有翻译文本"""
        # 更新按钮和标签文本
        self.table_label.setText(_("keyword_stats"))
        self.plot_label.setText(_("keyword_trend"))
        self.grouped_label.setText(_("similar_groups"))
        self.similarity_label.setText(_("similarity_threshold"))
        self.group_button.setText(_("group_keywords"))
        self.export_excel_button.setText(_("export_excel"))
        self.export_graph_button.setText(_("export_graph"))
        
        # 更新分组区域GroupBox标题
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if isinstance(item, QHBoxLayout):
                for j in range(item.count()):
                    widget = item.itemAt(j).widget()
                    if isinstance(widget, QGroupBox):
                        if "export" in widget.title().lower():
                            widget.setTitle(_("export"))
                        elif "similar" in widget.title().lower():
                            widget.setTitle(_("similar_groups"))
        
        # 更新表格标题
        if self.keyword_table.columnCount() > 0:
            current_headers = [self.keyword_table.horizontalHeaderItem(i).text() 
                            for i in range(self.keyword_table.columnCount())]
            if "keyword" in current_headers[0].lower() or "关键词" in current_headers[0]:
                years = current_headers[1:-1]  # 年份保持不变
                new_headers = [_("keyword")] + years + [_("total")]
                self.keyword_table.setHorizontalHeaderLabels(new_headers)
        
        # 更新图表标签 - 保留此代码以支持多语言图表标签
        if hasattr(self, 'keyword_plot') and self.keyword_plot.axes:
            self.keyword_plot.axes.set_xlabel(_("year"))
            self.keyword_plot.axes.set_ylabel(_("count"))
            self.keyword_plot.axes.set_title(_("keyword_trend"))
            self.keyword_plot.draw()