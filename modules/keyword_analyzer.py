from collections import defaultdict
import inflect
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class KeywordAnalyzer:
    """关键词分析模块，处理和分析文章关键词"""
    
    def __init__(self):
        self.p = inflect.engine()
        self.debug_info = []
        
    def singularize_keyword(self, keyword):
        """
        将关键词短语的最后一个词转换为单数形式
        同时，用空格替换连字符以确保格式一致
        
        参数:
            keyword (str): 要单数化的关键词短语
            
        返回:
            str: 单数化后的关键词短语
        """
        # 替换连字符为空格
        keyword = keyword.replace('-', ' ')
        
        words = keyword.split()
        if not words:
            return keyword
            
        # 仅将最后一个词单数化
        last_word = words[-1]
        singular_last_word = self.p.singular_noun(last_word)
        if singular_last_word:
            words[-1] = singular_last_word
            
        return ' '.join(words)
    
    def process_keywords(self, records):
        """
        处理记录中的关键词，转换为单数形式和小写
        
        参数:
            records (list): 记录字典列表
            
        返回:
            dict: 按年份组织的关键词统计
        """
        keyword_stats = defaultdict(lambda: defaultdict(int))
        
        for record in records:
            if 'PY' not in record:
                continue
                
            year = record['PY']
            keywords = []
            
            # 处理DE关键词
            if 'DE' in record:
                de_text = record['DE']
                de_keywords = [kw.strip() for kw in de_text.split(';') if kw.strip()]
                for kw in de_keywords:
                    processed_kw = self.singularize_keyword(kw.lower())
                    keywords.append(processed_kw)
                    keyword_stats[processed_kw][year] += 1
            
            # 处理ID关键词
            if 'ID' in record:
                id_text = record['ID']
                id_keywords = [kw.strip() for kw in id_text.split(';') if kw.strip()]
                for kw in id_keywords:
                    processed_kw = self.singularize_keyword(kw.lower())
                    keywords.append(processed_kw)
                    keyword_stats[processed_kw][year] += 1
            
            # 将处理后的关键词添加到记录中
            record['Keywords'] = keywords
        
        return dict(keyword_stats)
    
    def group_similar_keywords(self, keyword_stats, threshold=80):
        """
        将相似的关键词分组
        
        参数:
            keyword_stats (dict): 关键词统计数据
            threshold (int): 相似度阈值(0-100)
            
        返回:
            list: 每个组是一个包含相似关键词的列表
        """
        keywords = list(keyword_stats.keys())
        groups = []
        used = set()
        
        for keyword in keywords:
            if keyword in used:
                continue
                
            # 找出相似和未使用的关键词
            similar = process.extract(keyword, keywords, scorer=fuzz.token_sort_ratio)
            similar_keywords = [k for k, score in similar if score >= threshold and k not in used]
            
            if similar_keywords:
                groups.append(similar_keywords)
                used.update(similar_keywords)
                
        return groups
    
    def get_debug_info(self):
        """获取调试信息"""
        return self.debug_info
    
    def reset(self):
        """重置分析器状态"""
        self.debug_info = []