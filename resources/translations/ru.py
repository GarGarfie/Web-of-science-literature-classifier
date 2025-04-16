"""俄语翻译词典"""

# 通用文本
COMMON = {
    "language": "Язык:",
    "browse": "Обзор",
    "close": "Закрыть",
    "success": "Успех",
    "error": "Ошибка",
    "no_data": "Нет доступных данных",
    "export_success": "Данные экспортированы в {0}",
    "export_error": "Ошибка при экспорте данных: {0}",
    "year": "Год",
    "total": "Всего",
    "export_excel": "Экспорт в Excel",
    "export_csv": "Экспорт в CSV",
    "export_graph": "Экспорт графика",
}

# 主窗口文本
MAIN = {
    "app_title": "Инструмент анализа литературы Web of Science",
    "file_select": "Файлы не выбраны",
    "reset_all": "Сбросить все данные",
    "debug_info": "Просмотр отладочной информации",
    "tab_keywords": "Анализ ключевых слов",
    "tab_countries": "Анализ по странам",
    "import_complete": "Импорт завершен",
    "import_success": "Успешно импортировано {0} записей.",
    "reset_complete": "Сброс завершен",
    "reset_msg": "Все данные очищены.",
    "open_wos_files": "Открыть файлы Web of Science",
    "text_files": "Текстовые файлы", 
    "selected_files": "Выбранные файлы:"
}

# 关键词模块文本
KEYWORD = {
    "keyword_stats": "Статистика ключевых слов",
    "keyword_trend": "Тенденции ключевых слов",
    "similar_groups": "Группы похожих ключевых слов",
    "similarity_threshold": "Порог сходства:",
    "export": "Экспорт",
    "export_excel": "Экспорт в Excel",
    "export_graph": "Экспорт графика",
    "group_keywords": "Группировать ключевые слова",
    "keyword": "Ключевое слово",
    "count": "Количество"
}

# 国家模块文本
COUNTRY = {
    "country_stats": "Статистика публикаций по странам",
    "country_trend": "Тенденции публикаций по странам",
    "unknown_addresses": "Неидентифицированные адреса",
    "country_mapping": "Управление сопоставлением стран",
    "country": "Страна",
    "publication_count": "Количество публикаций",
    "add_mapping": "Добавить новое сопоставление стран",
    "original_name": "Исходное название страны:",
    "translated_name": "Соответствующее название:",
    "add": "Добавить",
    "update_analysis": "Обновить анализ"
}

# 合并所有字典，创建完整的翻译字典
TRANSLATIONS = {}
TRANSLATIONS.update(COMMON)
TRANSLATIONS.update(MAIN)
TRANSLATIONS.update(KEYWORD)
TRANSLATIONS.update(COUNTRY)