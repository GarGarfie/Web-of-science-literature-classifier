"""英语翻译词典"""

# 通用文本
COMMON = {
    "language": "Language:",
    "browse": "Browse",
    "close": "Close",
    "success": "Success",
    "error": "Error",
    "no_data": "No data available",
    "export_success": "Data exported to {0}",
    "export_error": "Error exporting data: {0}",
    "year": "Year",
    "total": "Total",
    "export_excel": "Export to Excel",
    "export_csv": "Export to CSV",
    "export_graph": "Export Graph",
}

# 主窗口文本
MAIN = {
    "app_title": "Web of Science Literature Analyzer",
    "file_select": "No files selected",
    "reset_all": "Reset All Data",
    "debug_info": "View Debug Info",
    "tab_keywords": "Keyword Analysis",
    "tab_countries": "Country Analysis",
    "import_complete": "Import Complete",
    "import_success": "Successfully imported {0} records.",
    "reset_complete": "Reset Complete",
    "reset_msg": "All data has been cleared.",
    "open_wos_files": "Open Web of Science Files",
    "text_files": "Text Files",
    "selected_files": "Selected files:"
}

# 关键词模块文本
KEYWORD = {
    "keyword_stats": "Keyword Statistics",
    "keyword_trend": "Keyword Trends",
    "similar_groups": "Similar Keyword Groups",
    "similarity_threshold": "Similarity Threshold:",
    "export": "Export",
    "export_excel": "Export to Excel",
    "export_graph": "Export to Graph",
    "group_keywords": "Group Keywords",
    "keyword": "Keyword",
    "count": "Count"
}

# 国家模块文本
COUNTRY = {
    "country_stats": "Country Publication Statistics",
    "country_trend": "Country Publication Trends",
    "unknown_addresses": "Unidentified Addresses",
    "country_mapping": "Country Mapping Management",
    "country": "Country",
    "publication_count": "Publication Count",
    "add_mapping": "Add New Country Mapping",
    "original_name": "Original Country Name:",
    "translated_name": "Corresponding Name:",
    "add": "Add",
    "update_analysis": "Update Analysis"
}

# 合并所有字典，创建完整的翻译字典
TRANSLATIONS = {}
TRANSLATIONS.update(COMMON)
TRANSLATIONS.update(MAIN)
TRANSLATIONS.update(KEYWORD)
TRANSLATIONS.update(COUNTRY)