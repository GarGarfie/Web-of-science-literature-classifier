#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from gui.main_window import MainWindow
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

def find_suitable_font():
    """查找适合的字体，优先考虑Times New Roman"""
    available_fonts = [f.name.lower() for f in fm.fontManager.ttflist]
    
    if 'times new roman' in available_fonts:
        return 'Times New Roman'
    
    # 尝试找到适合多语言的字体
    candidate_fonts = ['Arial', 'DejaVu Serif', 'Liberation Serif']
    for font in candidate_fonts:
        if font.lower() in available_fonts:
            return font
    
    # 如果都找不到，使用系统默认serif字体
    return 'serif'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置UI字体
    ui_font = QFont("Times New Roman", 10)
    app.setFont(ui_font)
    
    # 设置matplotlib全局字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 首选黑体
    plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())