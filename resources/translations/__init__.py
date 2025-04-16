"""
翻译模块 - 提供多语言支持
支持的语言：英语(en)、中文(zh)、俄语(ru)
"""

# 导入所有语言词典
from resources.translations import en, zh, ru

# 定义语言词典
ENGLISH = en.TRANSLATIONS
CHINESE = zh.TRANSLATIONS
RUSSIAN = ru.TRANSLATIONS

# 当前语言字典
_current_language = ENGLISH

def set_language(language_code):
    """设置当前使用的语言
    
    参数:
        language_code (str): 语言代码 ('en', 'zh', 'ru')
    """
    global _current_language
    if language_code == 'en':
        _current_language = ENGLISH
    elif language_code == 'zh':
        _current_language = CHINESE
    elif language_code == 'ru':
        _current_language = RUSSIAN
    else:
        _current_language = ENGLISH

def get_text(key, default=None):
    """获取当前语言的文本
    
    参数:
        key (str): 文本键
        default (str, optional): 如果键不存在，返回的默认值
        
    返回:
        str: 翻译的文本
    """
    if default is None:
        default = key
    return _current_language.get(key, default)

# 方便使用的别名
_ = get_text