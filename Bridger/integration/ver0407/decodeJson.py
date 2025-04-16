import json
import os
import pandas as pd
import re
import html
from collections import Counter

class decodeJson:
    def __init__(self):
        self.datas = []
        self.momo_datas = []
        self.reviewData = []
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """載入所有資料集"""
        # 載入舊數據集
        self._load_original_data()
        # 載入新的 momo 數據集
        self._load_momo_data()
        # 轉換為 DataFrame 便於處理
        self._create_dataframe()
        
    def _load_original_data(self):
        """載入原始資料集"""
        folderPath = 'schoolProject/xxSearchCrawler/output_comments/pchome'
        if not os.path.exists(folderPath):
            print(f"警告：舊資料集路徑不存在: {folderPath}")
            return
            
        try:
            for filename in os.listdir(folderPath):
                if not filename.endswith('.json'):
                    continue
                    
                filePath = os.path.join(folderPath, filename)
                try:
                    with open(filePath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.datas.append(data)
                except json.JSONDecodeError:
                    print(f"警告：無法解析 JSON 檔案: {filePath}")
                except Exception as e:
                    print(f"警告：讀取檔案時出錯: {filePath}, 錯誤: {str(e)}")
        except Exception as e:
            print(f"處理舊資料集時出錯: {str(e)}")
            
    def _load_momo_data(self):
        """載入 momo 資料集"""
        folderPath = 'schoolProject/xxSearchCrawler/output_comments/momo'
        if not os.path.exists(folderPath):
            print(f"警告：momo 資料集路徑不存在: {folderPath}")
            return
            
        try:
            for filename in os.listdir(folderPath):
                if not filename.endswith('.json'):
                    continue
                    
                filePath = os.path.join(folderPath, filename)
                try:
                    with open(filePath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.momo_datas.append(data)
                except json.JSONDecodeError:
                    print(f"警告：無法解析 momo JSON 檔案: {filePath}")
                except Exception as e:
                    print(f"警告：讀取 momo 檔案時出錯: {filePath}, 錯誤: {str(e)}")
        except Exception as e:
            print(f"處理 momo 資料集時出錯: {str(e)}")
    
    def _extract_reviews(self):
        """提取所有評論數據"""
        # 處理原始數據
        for jsn in self.datas:
            for product in jsn:
                if '評論' not in product:
                    continue
                    
                for review in product["評論"]:
                    if not isinstance(review, dict):
                        continue
                        
                    if "評論" in review and review["評論"] != '':
                        self.reviewData.append({
                            "產品名稱": review.get('產品名稱', '未知產品'),
                            "評論": self.clean_html_tags(review['評論']),
                            "星數": review.get('星數', ''),
                            "日期": review.get('日期', ''),
                            "平台來源": product.get('平台來源', '其他')
                        })
        
        # 處理 momo 數據
        for product_list in self.momo_datas:
            for product in product_list:
                if not isinstance(product, dict) or '評論' not in product:
                    continue
                    
                product_name = product.get('產品頭銜', '未知產品')
                platform = product.get('平台來源', 'momo')
                
                for review in product["評論"]:
                    if not isinstance(review, dict):
                        continue
                        
                    if "評論" in review and review["評論"] != '':
                        self.reviewData.append({
                            "產品名稱": review.get('產品名稱', product_name),
                            "評論": self.clean_html_tags(review['評論']),
                            "星數": review.get('星數', ''),
                            "日期": review.get('日期', ''),
                            "平台來源": platform
                        })
    
    def _create_dataframe(self):
        """轉換評論資料為 DataFrame"""
        self._extract_reviews()
        if not self.reviewData:
            self.df = pd.DataFrame(columns=["產品名稱", "評論", "星數", "日期", "平台來源"])
        else:
            self.df = pd.DataFrame(self.reviewData)
    
    def clean_html_tags(self, text):
        """清理 HTML 標籤"""
        if not isinstance(text, str):
            return ""
            
        text = re.sub(r'<[^>]+>', '', text)  # 移除 HTML tags
        text = html.unescape(text)           # 處理 HTML 實體
        return text
    
    def search_reviews(self, keywords):
        """使用關鍵字搜尋評論"""
        if self.df is None or self.df.empty:
            print("沒有可搜索的資料")
            return pd.DataFrame()
            
        # 如果是字符串列表，將其合併為一個查詢條件
        if isinstance(keywords, list):
            # 創建一個 OR 查詢條件 - 只要有任何一個關鍵字就匹配
            query = '|'.join([f"(?i){keyword}" for keyword in keywords])
        else:
            query = f"(?i){keywords}"
            
        # 搜尋產品名稱和評論
        filtered_df = self.df[
            self.df['產品名稱'].str.contains(query, regex=True, na=False) | 
            self.df['評論'].str.contains(query, regex=True, na=False)
        ]
        
        # 顯示搜索結果
        if filtered_df.empty:
            print(f"未找到匹配關鍵字 '{keywords}' 的評論")
        else:
            print(f"找到 {len(filtered_df)} 則關於 '{keywords}' 的評論")
        
        return filtered_df
    
    def makeSentence(self):
        """將所有篩選過的評論連接為文本"""
        if self.df is None or self.df.empty:
            return ""
            
        # 使用換行符連接所有評論
        return "\n".join(self.df['評論'].dropna().tolist())
    
    def get_platform_stats(self):
        """計算每個平台的評論數量"""
        if self.df is None or self.df.empty:
            return {}
            
        return dict(Counter(self.df['平台來源']))

    def readFile(self):
        """向後兼容方法"""
        return self.reviewData

# 測試代碼
if __name__ == "__main__":
    decoder = decodeJson()
    print(f"總共載入 {len(decoder.reviewData)} 則評論")
    print(f"平台統計: {decoder.get_platform_stats()}")
