import json
import os
import pandas as pd
import re  # 匯入正則表達式模組

class decodeJson:
    def __init__(self):
        self.datas = []
        self.text = ""
        self.reviews = []  # 存下來過濾後的評論清單

    def readFile(self):
        # Define a list of directories to read from
        folderPaths = [
            'schoolProject/xxSearchCrawler/output_comments/pchome',
            'schoolProject/xxSearchCrawler/output_comments/momo' # Add the momo directory
        ]
        self.datas = [] # Clear previous data if readFile is called multiple times
        for folderPath in folderPaths:
            print(f"Reading files from: {folderPath}") # Add logging
            if not os.path.isdir(folderPath):
                print(f"Warning: Directory not found - {folderPath}")
                continue
            for filename in os.listdir(folderPath):
                if filename.endswith(".json"):
                    filePath = os.path.join(folderPath, filename)
                    try:
                        with open(filePath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            # Ensure data is a list before extending
                            if isinstance(data, list):
                                self.datas.extend(data) # Use extend to add items from the loaded list
                            else:
                                print(f"Warning: Expected a list in {filePath}, but got {type(data)}. Skipping file.")
                    except json.JSONDecodeError:
                        print(f"Warning: Could not decode JSON from {filePath}")
                    except Exception as e:
                        print(f"Warning: Error processing file {filePath}: {e}")
        print(f"Finished reading. Total items loaded: {len(self.datas)}") # Add logging


    def makeSearchList(self):
        self.readFile()
        reviewData = []

        for item in self.datas:
            # 檢查 item 是否為字典且包含必要的鍵
            if isinstance(item, dict) and '評論' in item and isinstance(item['評論'], list):
                for review in item['評論']:
                    # 檢查 review 是否為字典且包含必要的鍵
                    if isinstance(review, dict) and all(k in review for k in ['評論', '產品名稱', '星數', '日期']):
                        reviewData.append({
                            "分類": item.get("分類", "N/A"),
                            "產品名稱": review['產品名稱'],
                            "評論": self.clean_html_tags(review['評論']),
                            "星數": review['星數'],
                            "日期": review['日期'],
                            "產品頭銜": item.get('產品頭銜', "N/A"),
                            "平台來源": item.get('平台來源', "N/A")
                        })
    
        return reviewData

    def clean_html_tags(self, text):
        return re.sub(r'<.*?>', '', text)
        
    def separate_review_from_product(self, text): #名琮
        """分離評論和產品名稱"""
        if not text:
            return ""
            
        # 使用冒號分割評論和產品名稱
        parts = text.split(':', 1)
        if len(parts) > 1:
            return parts[0].strip()  # 只返回冒號前的評論部分
        return text.strip()

    def containKeywords(self, keywords, str):
        contained = True
        for i in keywords:
            if i.lower() not in str.lower(): 
                contained = False
        return contained
    
    def search_reviews(self, keyword):
        all_reviews = self.makeSearchList()
        self.reviews = []  # 清空之前的結果
        self.text = ""

        for review in all_reviews:
            if self.containKeywords(keyword, review["產品名稱"]) or self.containKeywords(keyword, review["評論"]):
                
                self.reviews.append(review)
                # 只添加評論內容，不包括產品名稱 : 名琮
                if review['評論']:
                    self.text += "\n" + review['評論']
                
        print(self.text)
        return self.reviews  # 回傳 list

    def makeSentence(self):
        """返回純評論文本，不包含產品名稱"""
        # 確保返回的文本不包含產品名稱
        lines = self.text.split('\n')
        clean_lines = [self.separate_review_from_product(line) for line in lines]
        return '\n'.join(clean_lines)
