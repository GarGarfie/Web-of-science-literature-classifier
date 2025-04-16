import re
import os
import json
from collections import defaultdict

class CountryAnalyzer:
    """国家分析模块，处理和分析文章的国家信息"""
    
    def __init__(self):
        self.countries = defaultdict(lambda: defaultdict(int))
        self.unknown_addresses = set()
        self.debug_info = []
        
        # 加载国家映射
        self.user_country_mapping = self.load_user_country_mapping()
        self.default_country_mapping = self._get_default_country_mapping()
        self.country_mapping = {**self.default_country_mapping, **self.user_country_mapping}
    
    def load_user_country_mapping(self):
        """加载用户自定义的国家映射"""
        mapping_file = 'user_country_mapping.json'
        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_user_country_mapping(self):
        """保存用户自定义的国家映射"""
        mapping_file = 'user_country_mapping.json'
        try:
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_country_mapping, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def add_country_mapping(self, original_name, translated_name):
        """添加新的国家映射"""
        self.user_country_mapping[original_name] = translated_name
        self.country_mapping[original_name] = translated_name
        self.save_user_country_mapping()
    
    def _get_default_country_mapping(self):
        """获取默认的国家名称映射"""
        # 这里应该包含counter.py中的完整映射
        return {
            # 美国
            "USA": "United States", "United States": "United States", "U.S.A.": "United States", "U.S.A": "United States", 
            "United States of America": "United States", "US": "United States", "U S A": "United States", "U S": "United States",
            "United States America": "United States", "america": "United States", "America": "United States", "美国": "United States",
            # 中国
            "China": "China", "P.R.China": "China", "P.R. China": "China", 
            "People's Republic of China": "China", "PR China": "China", "Peoples R China": "China",
            "Peoples Republic China": "China", "PRC": "China",
            # 英国
            "UK": "United Kingdom", "United Kingdom": "United Kingdom", "England": "United Kingdom", "Scotland": "United Kingdom", 
            "Wales": "United Kingdom", "Northern Ireland": "United Kingdom", "Great Britain": "United Kingdom", "Britain": "United Kingdom",
            # 德国
            "Germany": "German", "Deutschland": "German", "Federal Republic of Germany": "German",
            # 日本
            "Japan": "Japanese", "Nippon": "Japanese",
            # 加拿大 (Canada) (Канада)
            "Canada": "Canada",
            # 澳大利亚 (Australia) (Австралия)
            "Australia": "Australia", "Commonwealth of Australia": "Australia",
            # 法国 (France) (Франция)
            "France": "France", "République Française": "France", "Republique Francaise": "France",
            # 意大利 (Italy) (Италия)
            "Italy": "Italy", "Italia": "Italy",
            # 西班牙 (Spain) (Испания)
            "Spain": "Spain", "España": "Spain", "Espana": "Spain",
            # 巴西 (Brazil) (Бразилия)
            "Brazil": "Brazil", "Brasil": "Brazil",
            # 荷兰 (Netherlands) (Нидерланды)
            "Netherlands": "Netherlands", "The Netherlands": "Netherlands", "Holland": "Netherlands",
            # 韩国 (South Korea) (Южная Корея)
            "South Korea": "South Korea", "Korea": "South Korea", "Republic of Korea": "South Korea", "S Korea": "South Korea",
            # 瑞典 (Sweden) (Швеция)
            "Sweden": "Sweden",
            # 瑞士 (Switzerland) (Швейцария)
            "Switzerland": "Switzerland", "Schweiz": "Switzerland", "Suisse": "Switzerland",
            # 印度 (India) (Индия)
            "India": "India", "Republic of India": "India",
            # 台湾省(中国) (Taiwan Province (China)) (Провинция Тайвань (Китай))
            "Taiwan": "Taiwan Province (China)", "Republic of China": "Taiwan Province (China)", "Taiwan ROC": "Taiwan Province (China)", 
            "Chinese Taipei": "Taiwan Province (China)", "Taipei": "Taiwan Province (China)", "TAIWAN": "Taiwan Province (China)",
            # 哈萨克斯坦 (Kazakhstan) (Казахстан)
            "Kazakhstan": "Kazakhstan", 
            # 新加坡 (Singapore) (Сингапур)
            "Singapore": "Singapore", "Republic of Singapore": "Singapore",
            # 比利时 (Belgium) (Бельгия)
            "Belgium": "Belgium", "Belgique": "Belgium", "Belgie": "Belgium",
            # 丹麦 (Denmark) (Дания)
            "Denmark": "Denmark",
            # 俄罗斯 (Russia) (Россия)
            "Russia": "Russia", "Russian Federation": "Russia", "USSR": "Russia", 
            "Soviet Union": "Russia",
            # 挪威 (Norway) (Норвегия)
            "Norway": "Norway",
            # 芬兰 (Finland) (Финляндия)
            "Finland": "Finland",
            # 奥地利 (Austria) (Австрия)
            "Austria": "Austria",
            # 波兰 (Poland) (Польша)
            "Poland": "Poland",
            # 土耳其 (Turkey) (Турция)
            "Turkey": "Turkey", "Turkiye": "Turkey",
            # 以色列 (Israel) (Израиль)
            "Israel": "Israel",
            # 墨西哥 (Mexico) (Мексика)
            "Mexico": "Mexico",
            # 葡萄牙 (Portugal) (Португалия)
            "Portugal": "Portugal",
            # 新西兰 (New Zealand) (Новая Зеландия)
            "New Zealand": "New Zealand",
            # 希腊 (Greece) (Греция)
            "Greece": "Greece", "Hellas": "Greece",
            # 爱尔兰 (Ireland) (Ирландия)
            "Ireland": "Ireland", "Republic of Ireland": "Ireland", "Eire": "Ireland",
            # 捷克 (Czech Republic) (Чехия)
            "Czech Republic": "Czech Republic", "Czechia": "Czech Republic", "Czech": "Czech Republic",
            # 匈牙利 (Hungary) (Венгрия)
            "Hungary": "Hungary",
            # 南非 (South Africa) (Южная Африка)
            "South Africa": "South Africa", "Republic of South Africa": "South Africa", "RSA": "South Africa",
            # 阿根廷 (Argentina) (Аргентина)
            "Argentina": "Argentina",
            # 智利 (Chile) (Чили)
            "Chile": "Chile",
            # 马来西亚 (Malaysia) (Малайзия)
            "Malaysia": "Malaysia",
            # 泰国 (Thailand) (Таиланд)
            "Thailand": "Thailand",
            # 埃及 (Egypt) (Египет)
            "Egypt": "Egypt", "Arab Republic of Egypt": "Egypt",
            # 沙特阿拉伯 (Saudi Arabia) (Саудовская Аравия)
            "Saudi Arabia": "Saudi Arabia", "KSA": "Saudi Arabia", "Saudi": "Saudi Arabia",
            # 伊朗 (Iran) (Иран)
            "Iran": "Iran", "Islamic Republic of Iran": "Iran",
            # 越南 (Vietnam) (Вьетнам)
            "Vietnam": "Vietnam", "Viet Nam": "Vietnam",
            # 阿联酋 (United Arab Emirates) (Объединенные Арабские Эмираты)
            "United Arab Emirates": "United Arab Emirates", "UAE": "United Arab Emirates",
            # 卡塔尔 (Qatar) (Катар)
            "Qatar": "Qatar",
            # 科威特 (Kuwait) (Кувейт)
            "Kuwait": "Kuwait",
            # 巴基斯坦 (Pakistan) (Пакистан)
            "Pakistan": "Pakistan",
            # 印度尼西亚 (Indonesia) (Индонезия)
            "Indonesia": "Indonesia",
            # 菲律宾 (Philippines) (Филиппины)
            "Philippines": "Philippines",
            # 哥伦比亚 (Colombia) (Колумбия)
            "Colombia": "Colombia",
            # 秘鲁 (Peru) (Перу)
            "Peru": "Peru",
            # 尼日利亚 (Nigeria) (Нигерия)
            "Nigeria": "Nigeria",
            # 摩洛哥 (Morocco) (Марокко)
            "Morocco": "Morocco",
            # 乌克兰 (Ukraine) (Украина)
            "Ukraine": "Ukraine",
            # 克罗地亚 (Croatia) (Хорватия)
            "Croatia": "Croatia",
            # 斯洛伐克 (Slovakia) (Словакия)
            "Slovakia": "Slovakia", "Slovak Republic": "Slovakia",
            # 斯洛文尼亚 (Slovenia) (Словения)
            "Slovenia": "Slovenia",
            # 塞尔维亚 (Serbia) (Сербия)
            "Serbia": "Serbia",
            # 罗马尼亚 (Romania) (Румыния)
            "Romania": "Romania",
            # 保加利亚 (Bulgaria) (Болгария)
            "Bulgaria": "Bulgaria",
            # 爱沙尼亚 (Estonia) (Эстония)
            "Estonia": "Estonia",
            # 立陶宛 (Lithuania) (Литва)
            "Lithuania": "Lithuania",
            # 拉脱维亚 (Latvia) (Латвия)
            "Latvia": "Latvia",
            # 卢森堡 (Luxembourg) (Люксембург)
            "Luxembourg": "Luxembourg", "Luxemburg": "Luxembourg",
            # 冰岛 (Iceland) (Исландия)
            "Iceland": "Iceland",
            # 澳门 (Macau) (Макао)
            "Macau": "Macau (China)", "Macao": "Macau (China)",
            # 香港 (Hong Kong) (Гонконг)
            "Hong Kong": "Hong Kong (China)", "HK": "Hong Kong (China)", "Hongkong": "Hong Kong (China)"
        }
    
    def analyze_countries(self, records):
        """
        从记录中分析国家信息
        
        参数:
            records (list): 记录字典列表
            
        返回:
            dict: 按国家和年份组织的统计
        """
        # 清除以前的结果
        self.countries = defaultdict(lambda: defaultdict(int))
        self.unknown_addresses = set()
        
        records_with_countries = 0
        
        for record in records:
            if 'PY' not in record:
                continue
                
            year = record['PY']
            countries = set()
            
            # 从C1字段提取国家
            if 'C1' in record:
                c1_countries, c1_addresses = self.extract_countries_from_address(record['C1'])
                countries.update(c1_countries)
                self.unknown_addresses.update(c1_addresses)
            
            # 从RP字段提取国家作为备用
            if 'RP' in record and not countries:
                rp_countries, rp_addresses = self.extract_countries_from_address(record['RP'])
                countries.update(rp_countries)
                self.unknown_addresses.update(rp_addresses)
            
            # 记录找到的国家
            if countries:
                records_with_countries += 1
                for country in countries:
                    self.countries[country][year] += 1
        
        self.debug_info.append(f"找到国家的记录数: {records_with_countries}")
        self.debug_info.append(f"找到的国家数: {len(self.countries)}")
        
        return dict(self.countries)
    
    def extract_countries_from_address(self, address_text):
        """
        从地址文本中提取国家名称
        
        参数:
            address_text (str): 地址文本
            
        返回:
            tuple: (国家集合, 未识别地址集合)
        """
        countries = set()
        unknown_addresses = set()
        
        # 按分号和换行符分割地址
        institutions = []
        for part in address_text.split(';'):
            for subpart in part.split('\n'):
                if subpart.strip():
                    institutions.append(subpart.strip())
        
        for institution in institutions:
            country_found = False
            
            # 方法1: 查找完整的国家名称(不区分大小写)
            for country_name, local_name in self.country_mapping.items():
                pattern = r'\b' + re.escape(country_name) + r'\b'
                if re.search(pattern, institution, re.IGNORECASE):
                    countries.add(local_name)
                    country_found = True
                    break
            
            # 方法2: 查找地址末尾的国家名称
            if not country_found:
                # 移除括号内容
                clean_institution = re.sub(r'\([^)]*\)', '', institution)
                
                # 按逗号分割
                parts = clean_institution.split(',')
                for i in range(len(parts)-1, -1, -1):
                    part = parts[i].strip()
                    for country_name, local_name in self.country_mapping.items():
                        if part.lower() == country_name.lower():
                            countries.add(local_name)
                            country_found = True
                            break
                    if country_found:
                        break
            
            # 方法3: 查找邮政编码模式
            if not country_found:
                # 美国邮编
                if re.search(r'\b\d{5}(-\d{4})?\b', institution):
                    countries.add("United States")
                    country_found = True
                # 其他邮编和识别逻辑...
            
            # 如果未找到国家，存储该地址
            if not country_found:
                unknown_addresses.add(institution)
        
        return countries, unknown_addresses
    
    def get_countries_data(self):
        """获取国家统计数据"""
        return dict(self.countries)
    
    def get_unknown_addresses(self):
        """获取未识别的地址"""
        return list(self.unknown_addresses)
    
    def get_debug_info(self):
        """获取调试信息"""
        return self.debug_info
    
    def reset(self):
        """重置分析器状态"""
        self.countries = defaultdict(lambda: defaultdict(int))
        self.unknown_addresses = set()
        self.debug_info = []