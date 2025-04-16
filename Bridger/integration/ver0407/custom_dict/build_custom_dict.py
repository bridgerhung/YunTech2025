#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import re
import jieba
import jieba.posseg as pseg
from collections import Counter, defaultdict

class ECommerceDict:
    def __init__(self):
        self.comment_words = []
        self.product_words = []
        self.comment_phrases = []
        self.vocab = defaultdict(int)
        self.product_vocab = defaultdict(int)
        self.ecommerce_terms = [
            "品質", "包裝", "物流", "服務", "CP值", "免運", "保固", "寄送", "出貨", "收到", 
            "收件", "下單", "評價", "星等", "評分", "好用", "實用", "便宜", "划算", "超值", 
            "耐用", "安裝", "設定", "操作", "方便", "快速", "穩定", "問題", "有效", "效果",
            "金錢", "效能", "外型", "大小", "尺寸", "重量", "續航", "噪音", "溫度", "功能",
            "價格", "便利", "優惠", "折扣", "退貨", "退款", "送貨", "材質", "運作", "運行",
            "體積", "外觀", "風扇", "喜歡", "推薦", "電池", "螢幕", "配件", "保護", "兩年"
        ]

        # 電商常見產品特徵詞
        self.product_features = [
            "穩壓", "不斷電", "在線式", "互動式", "離線式", "真正", "機殼", "液晶", "螢幕", "電池",
            "純正弦波", "突波", "雷擊", "保護", "吸收", "充電", "功率", "容量", "風扇", "噪音",
            "台灣製造", "MIT", "外銷", "智能", "保固", "零件", "備用", "自動", "控制", "USB",
            "熱抽換", "綠能", "節能", "延遲", "啟動", "輸出", "輸入", "插座", "LCD", "LED",
            "溫度", "顯示", "過載", "短路", "防火", "穩定", "跳脫", "防護", "電流", "電壓",
            "自動", "手動", "耐用", "高效", "監控", "軟體", "程式", "正弦波", "模擬", "轉換"
        ]
        
        # 電商評價常用情感詞
        self.sentiment_words = [
            "好", "壞", "爛", "佳", "優", "差", "棒", "糟", "讚", "推",
            "快", "慢", "高", "低", "強", "弱", "大", "小", "輕", "重",
            "穩", "不穩", "靜", "吵", "熱", "冷", "易", "難", "順", "卡",
            "新", "舊", "硬", "軟", "亮", "暗", "實", "虛", "貴", "便宜",
            "滿意", "不滿", "失望", "驚喜", "可靠", "不可靠", "簡單", "複雜", "清晰", "模糊",
            "耐用", "易壞", "方便", "麻煩", "安靜", "吵雜", "漂亮", "醜陋", "實在", "虛假",
            "舒適", "不適", "平穩", "震動", "幫助", "阻礙", "喜歡", "討厭", "愛", "恨"
        ]

    def load_json(self, json_path):
        """讀取商品評論JSON檔案"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def process_review_comments(self, data):
        """處理評論內容"""
        for item in data:
            # 提取產品名稱並分詞
            product_title = item.get("產品頭銜", "")
            if product_title:
                self.product_words.extend(jieba.lcut(product_title))
                
            # 提取產品規格、介紹
            product_spec = item.get("產品規格", "")
            product_intro = item.get("產品介紹", "")
            if product_spec and product_spec != "N/A":
                self.product_words.extend(jieba.lcut(product_spec))
            if product_intro:
                self.product_words.extend(jieba.lcut(product_intro))
                
            # 處理評論
            reviews = item.get("評論", [])
            for review in reviews:
                comment = review.get("評論", "")
                # 只處理非空評論
                if comment and len(comment.strip()) > 0:
                    # 清理評論
                    comment = self._clean_text(comment)
                    
                    # 提取常見短語
                    phrases = self._extract_phrases(comment)
                    self.comment_phrases.extend(phrases)
                    
                    # 分詞
                    words = jieba.lcut(comment)
                    self.comment_words.extend(words)

    def _clean_text(self, text):
        """清理文本"""
        text = re.sub(r'<br/>', '', text)
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        return text.strip()
    
    def _extract_phrases(self, text):
        """提取評論中常見的短語"""
        phrases = []
        
        # 使用正則表達式提取可能的多字詞語
        pattern = r'([a-zA-Z0-9\u4e00-\u9fff]{2,6})([的得地]?)([a-zA-Z0-9\u4e00-\u9fff]{1,4})'
        matches = re.findall(pattern, text)
        for match in matches:
            phrase = ''.join(match)
            if 2 <= len(phrase) <= 8:  # 限制短語長度
                phrases.append(phrase)
                
        return phrases
    
    def analyze_word_frequency(self):
        """分析詞頻"""
        # 評論詞頻
        comment_counter = Counter(self.comment_words)
        for word, count in comment_counter.items():
            if len(word) > 1:  # 只考慮多字詞
                self.vocab[word] += count
        
        # 產品詞頻
        product_counter = Counter(self.product_words)
        for word, count in product_counter.items():
            if len(word) > 1:  # 只考慮多字詞
                self.product_vocab[word] += count
                
        # 短語詞頻
        phrase_counter = Counter(self.comment_phrases)
        for phrase, count in phrase_counter.items():
            if len(phrase) > 1 and count > 1:  # 只考慮多次出現的短語
                self.vocab[phrase] += count * 2  # 短語權重加倍
    
    def load_all_json_files(self, directory):
        """讀取目錄下的所有JSON檔案並處理評論"""
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json') and file.startswith('output_'):
                    try:
                        json_path = os.path.join(root, file)
                        data = self.load_json(json_path)
                        self.process_review_comments(data)
                        print(f"已處理檔案: {file}")
                    except Exception as e:
                        print(f"處理檔案 {file} 時發生錯誤: {str(e)}")
    
    def generate_custom_dict(self, output_path, count_threshold=2):
        """生成自定義詞典"""
        self.analyze_word_frequency()
        
        # 合併詞彙
        all_words = {}
        for word, count in self.vocab.items():
            if count >= count_threshold and len(word) > 1:
                all_words[word] = count
                
        for word, count in self.product_vocab.items():
            if count >= count_threshold and len(word) > 1:
                all_words[word] = max(all_words.get(word, 0), count)
                
        # 添加預定義的詞彙
        for word in self.ecommerce_terms:
            all_words[word] = max(all_words.get(word, 0), 10)
            
        for word in self.product_features:
            all_words[word] = max(all_words.get(word, 0), 8)
            
        for word in self.sentiment_words:
            all_words[word] = max(all_words.get(word, 0), 6)
            
        # 寫入詞典 - 修正格式，僅包含詞語和詞頻，不包含詞性
        with open(output_path, 'w', encoding='utf-8') as f:
            for word, count in sorted(all_words.items(), key=lambda x: x[1], reverse=True):
                # Jieba 詞典格式: 詞語 詞頻
                f.write(f"{word} {count}\n")
                
        print(f"自定義詞典已生成: {output_path}")
        print(f"詞典總詞數: {len(all_words)}")
        
    def generate_stopwords(self, output_path):
        """生成停用詞表"""
        stopwords = [
            "的", "了", "和", "是", "就", "都", "而", "及", "與", "著",
            "或", "一個", "那個", "這個", "這麼", "那麼", "如此", "只是", "因為", "所以",
            "然後", "接著", "可以", "可能", "應該", "需要", "必須", "一定", "大概", "也許",
            "啊", "阿", "哦", "哈", "嗯", "呢", "吧", "啦", "喔", "欸",
            "這", "那", "這些", "那些", "有的", "有些", "太", "非常", "很", "真的", "超",
            "不過", "但是", "雖然", "然而", "不", "沒", "不是", "沒有", "得", "地", "比較",
            "還", "還是", "其實", "大概", "大家", "目前", "而且", "什麼", "怎麼", "如何", "為何",
            "有點", "有些", "突然", "忽然", "已經", "曾經", "剛剛", "一直", "正在", "將要", "能夠",
            "無法", "不能", "絕對", "肯定", "覺得", "認為", "找到", "看到", "聽到", "想到", "出現",
            "一下", "一些", "一樣", "不少", "不只", "不要", "以及", "先前", "又", "只有", "周圍",
            "哪裡", "因此", "尤其", "很多", "想要", "我", "你", "他", "她", "它", "我們", "你們", "他們",
            "自己", "本身", "哪個", "誰", "什麼", "哪", "啥", "多少", "如果", "若", "或者"
        ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for word in stopwords:
                f.write(word + '\n')
                
        print(f"停用詞表已生成: {output_path}")
        print(f"停用詞總數: {len(stopwords)}")

if __name__ == "__main__":
    dict_builder = ECommerceDict()
    
    # 處理所有評論JSON檔案
    json_dir = "/home/user/YunTech2025/schoolProject/xxSearchCrawler/output_comments"
    dict_builder.load_all_json_files(json_dir)
    
    # 生成自定義詞典和停用詞表
    dict_builder.generate_custom_dict("/home/user/YunTech2025/Bridger/integration/ver0407/custom_dict/ecommerce_dict.txt")
    dict_builder.generate_stopwords("/home/user/YunTech2025/Bridger/integration/ver0407/custom_dict/ecommerce_stopwords.txt")