import json
import os
import pandas as pd
import re  # 匯入正則表達式模組
import html

class decodeJson:
    def __init__(self):
        self.datas =[]
        self.reviewData =[]
    def readFile(self):
        folderPath = 'schoolProject/xxSearchCrawler/pchome'

        for filename in os.listdir(folderPath):
            filePath = os.path.join(folderPath, filename)
            with open(filePath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.datas.append(data)
        for jsn in self.datas:
            for product in jsn:
                for review in product["評論"]:
                    if review["評論"] is not '':
                        self.reviewData.append({
                            "產品名稱": review['產品名稱'],
                            "評論": self.clean_html_tags(review['評論']),
                            "星數": review['星數'],
                            "日期": review['日期']
                        })
        return self.reviewData
    
    def clean_html_tags(self, text):
        text = re.sub(r'<[^>]+>', '', text)  # 移除 HTML tags 像 <br/>、<div> 等
        text = html.unescape(text)          # 將 &quot; 轉成 "，&amp; 轉成 & 等
        return text


decoder =decodeJson()
print(decoder.readFile())
