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
        folderPath = 'schoolProject/xxSearchCrawler/output_comments'
        for filename in os.listdir(folderPath):
            if filename.endswith(".json"):
                filePath = os.path.join(folderPath, filename)
                with open(filePath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.datas.append(data)

    def makeSearchList(self):
        self.readFile()
        reviewData = []

        for data in self.datas:
            for product in data:
                for review in product['評論']:
                    reviewData.append({
                        "分類": product["分類"],
                        "產品名稱": review['產品名稱'],
                        "評論": self.clean_html_tags(review['評論']),
                        "星數": review['星數'],
                        "日期": review['日期'],
                        "產品頭銜": product['產品頭銜'],
                        "平台來源": product['平台來源']
                    })

        return reviewData

    def clean_html_tags(self, text):
        return re.sub(r'<.*?>', '', text)


    def containKeywords(self, keywords, str):
        contained =True
        for i in keywords:
            if i.lower() not in str.lower(): contained =False
        return contained
    
    def search_reviews(self, keyword):
        all_reviews = self.makeSearchList()
        self.reviews = []  # 清空之前的結果
        self.text = ""

        for review in all_reviews:
            if self.containKeywords(keyword, review["產品名稱"]):
                
                self.reviews.append(review)
                self.text += "\n" + (review['評論'] if review["評論"] is not '' else '')  + ":" +review["產品名稱"]
                
        print(self.text)
        return self.reviews  # 回傳 list

    def makeSentence(self):
        return self.text



  # 返回過濾後的評論資料框
