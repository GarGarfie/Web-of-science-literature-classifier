import re
import os
from collections import defaultdict
from queue import Queue

class WoSFileParser:
    """Web of Science文件解析器，从文本文件中提取记录"""
    
    def __init__(self):
        self.records = []
        self.debug_info = []
        self.processed_files = []
        
    def parse_file(self, filepath, progress_queue=None):
        """
        解析Web of Science导出的文本文件
        
        参数:
            filepath (str): 文本文件路径
            progress_queue (Queue, optional): 进度更新队列
            
        返回:
            int: 解析的记录数
        """
        # 检查文件是否已处理
        if filepath in self.processed_files:
            self.debug_info.append(f"文件 {filepath} 已处理过，跳过")
            return 0
            
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 记录已处理文件
            self.processed_files.append(filepath)
            
            # 添加调试信息
            self.debug_info.append(f"读取文件 {os.path.basename(filepath)} 成功")
            
            # 通过 'PT J' 分割文章
            articles = re.split(r'PT J\n', content)
            
            # 记录处理前的记录数
            previous_count = len(self.records)
            
            total_articles = len(articles)
            
            for i, article in enumerate(articles):
                if not article.strip():
                    continue
                
                # 提取记录数据
                record = {}
                current_field = None
                
                for line in article.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                        
                    # 检查是否是新字段
                    if re.match(r'^[A-Z][A-Z](\s|\t)', line):
                        current_field = line[:2]
                        record[current_field] = line[3:].strip()
                    # 字段的延续
                    elif current_field:
                        record[current_field] += " " + line
                
                if record:
                    self.records.append(record)
                
                # 更新进度
                if progress_queue and total_articles > 0:
                    progress_queue.put((i + 1) / total_articles * 100)
            
            # 返回新增记录数
            return len(self.records) - previous_count
            
        except Exception as e:
            error_msg = f"解析文件 {os.path.basename(filepath)} 时出错: {str(e)}"
            self.debug_info.append(error_msg)
            return 0
    
    def get_records(self):
        """获取所有解析的记录"""
        return self.records
    
    def get_processed_files(self):
        """获取已处理的文件列表"""
        return self.processed_files
    
    def get_debug_info(self):
        """获取调试信息"""
        return self.debug_info
    
    def reset(self):
        """重置解析器状态"""
        self.records = []
        self.debug_info = []
        self.processed_files = []