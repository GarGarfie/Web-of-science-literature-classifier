"""中文翻译词典"""

# 通用文本
COMMON = {
    "language": "语言:",
    "browse": "浏览",
    "close": "关闭",
    "success": "成功",
    "error": "错误",
    "no_data": "没有可用数据",
    "export_success": "数据已导出到 {0}",
    "export_error": "导出数据时发生错误: {0}",
    "year": "年份",
    "total": "总计",
    "export_excel": "导出到Excel",
    "export_csv": "导出到CSV",
    "export_graph": "导出图表",
}

# 主窗口文本
MAIN = {
    "app_title": "Web of Science 文献分析工具",
    "file_select": "未选择文件",
    "reset_all": "重置所有数据",
    "debug_info": "查看调试信息",
    "tab_keywords": "关键词分析",
    "tab_countries": "国家分析",
    "import_complete": "导入完成",
    "import_success": "成功导入 {0} 条记录。",
    "reset_complete": "重置完成",
    "reset_msg": "所有数据已清除。",
    "open_wos_files": "打开Web of Science文件",
    "text_files": "文本文件",
    "selected_files": "已选择文件:"
}

# 关键词模块文本
KEYWORD = {
    "keyword_stats": "关键词统计",
    "keyword_trend": "Keyword Trend",
    "similar_groups": "相似关键词分组",
    "similarity_threshold": "相似度阈值:",
    "export": "导出",
    "export_excel": "导出为Excel表格",
    "export_graph": "导出图片",
    "group_keywords": "分组关键词",
    "keyword": "关键词",
    "count": "Publication Count"
}

# 国家模块文本
COUNTRY = {
    "country_stats": "国家出版统计",
    "country_trend": "国家出版趋势",
    "unknown_addresses": "未识别地址",
    "country_mapping": "国家映射管理",
    "country": "国家",
    "publication_count": "出版数量",
    "add_mapping": "添加新的国家映射",
    "original_name": "原始国家名称:",
    "translated_name": "对应中文名称:",
    "add": "添加",
    "update_analysis": "重新分析"
}

# 合并所有字典，创建完整的翻译字典
TRANSLATIONS = {}
TRANSLATIONS.update(COMMON)
TRANSLATIONS.update(MAIN)
TRANSLATIONS.update(KEYWORD)
TRANSLATIONS.update(COUNTRY)