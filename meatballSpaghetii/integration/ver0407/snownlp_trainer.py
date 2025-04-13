#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import re
import pandas as pd
from snownlp import SnowNLP
from snownlp.sentiment import Sentiment
import jieba
import pickle
from collections import defaultdict
from tqdm import tqdm
import opencc

class SentimentTrainer:
    def __init__(self, train_dir='model_training', 
                 neg_file='neg.txt', pos_file='pos.txt',
                 model_path='sentiment.marshal'):
        """初始化情感分析訓練器"""
        self.train_dir = train_dir
        self.neg_file = os.path.join(train_dir, neg_file)
        self.pos_file = os.path.join(train_dir, pos_file)
        self.model_path = os.path.join(train_dir, model_path)
        
        # 創建訓練目錄
        if not os.path.exists(train_dir):
            os.makedirs(train_dir)
            
        # 繁簡轉換
        self.converter = opencc.OpenCC('tw2sp')
        
        # 標記數據
        self.labeled_data = []
        
        print("情感模型訓練器初始化完成")
    
    def preprocess_text(self, text):
        """預處理文本"""
        if not text:
            return ""
        
        # 移除HTML標籤
        text = re.sub(r'<[^>]+>', '', text)
        
        # 移除非中文、英文、數字的字符，但保留基本標點符號
        text = re.sub(r'[^\u4e00-\u9fff\w\s.,!?，。！？、]', '', text)
        
        # 繁體轉簡體（SnowNLP對簡體中文效果較好）
        text = self.converter.convert(text)
        
        return text.strip()
    
    def extract_reviews_from_json(self, json_dir, min_length=5):
        """從JSON文件中提取評論數據"""
        reviews_data = []
        
        for filename in tqdm(os.listdir(json_dir)):
            if not filename.endswith('.json'):
                continue
                
            file_path = os.path.join(json_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for product in data:
                    for review in product['評論']:
                        review_text = review.get('評論', '')
                        star_rating = review.get('星數', 0)
                        
                        if not review_text or len(review_text) < min_length:
                            continue
                            
                        processed_text = self.preprocess_text(review_text)
                        
                        if processed_text:
                            reviews_data.append({
                                'text': processed_text,
                                'rating': star_rating
                            })
            except Exception as e:
                print(f"處理文件 {filename} 時出錯: {str(e)}")
        
        print(f"已提取 {len(reviews_data)} 條評論")
        return reviews_data
    
    def auto_label_reviews(self, reviews_data, positive_threshold=4, negative_threshold=2):
        """根據評分自動標記情感"""
        positive_reviews = []
        negative_reviews = []
        
        for review in reviews_data:
            text = review['text']
            rating = review['rating']
            
            if rating >= positive_threshold:
                positive_reviews.append(text)
            elif rating <= negative_threshold:
                negative_reviews.append(text)
        
        print(f"自動標記結果: 正面評論 {len(positive_reviews)} 條, 負面評論 {len(negative_reviews)} 條")
        return positive_reviews, negative_reviews
    
    def manual_label_review(self, review_text):
        """手動標記單個評論的情感"""
        print("\n" + "=" * 50)
        print(f"評論: {review_text}")
        
        while True:
            choice = input("請標記情感 (p: 正面, n: 負面, s: 跳過): ").lower()
            if choice == 'p':
                return 'positive'
            elif choice == 'n':
                return 'negative'
            elif choice == 's':
                return 'skip'
            else:
                print("無效輸入，請重試")
    
    def interactive_labeling(self, reviews_data, sample_size=100):
        """交互式標記評論情感"""
        import random
        
        if len(reviews_data) > sample_size:
            reviews_sample = random.sample(reviews_data, sample_size)
        else:
            reviews_sample = reviews_data
        
        positive_reviews = []
        negative_reviews = []
        
        for review in reviews_sample:
            label = self.manual_label_review(review['text'])
            if label == 'positive':
                positive_reviews.append(review['text'])
            elif label == 'negative':
                negative_reviews.append(review['text'])
        
        return positive_reviews, negative_reviews
    
    def save_labeled_data(self, positive_reviews, negative_reviews):
        """保存標記好的評論數據"""
        # 寫入正面評論
        with open(self.pos_file, 'w', encoding='utf-8') as f:
            for review in positive_reviews:
                f.write(review + '\n')
        
        # 寫入負面評論
        with open(self.neg_file, 'w', encoding='utf-8') as f:
            for review in negative_reviews:
                f.write(review + '\n')
        
        print(f"已將標記數據保存至 {self.pos_file} 和 {self.neg_file}")
    
    def train_sentiment_model(self):
        """訓練情感分析模型"""
        print("開始訓練情感分析模型...")
        sentiment = Sentiment()
        
        # 訓練模型
        sentiment.train(self.neg_file, self.pos_file)
        
        # 保存模型
        sentiment.save(self.model_path)
        print(f"模型訓練完成，已保存至 {self.model_path}")
        
    def test_sentiment_model(self, test_texts=None):
        """測試訓練好的情感模型"""
        from snownlp import SnowNLP
        import importlib
        
        # 確保模型被重新載入
        import snownlp.sentiment as sentiment
        importlib.reload(sentiment)
        
        if test_texts is None:
            test_texts = [
                "產品很好用，非常滿意",
                "速度很快，效能良好",
                "很失望，產品經常沒反應",
                "不推薦，用了一個月就壞了",
                "CP值很高，推薦購買"
            ]
        
        print("\n" + "=" * 50)
        print("測試情感分析結果:")
        
        for text in test_texts:
            s = SnowNLP(self.preprocess_text(text))
            sentiment_score = s.sentiments
            sentiment_level = "正面" if sentiment_score > 0.5 else "負面"
            print(f"評論: {text}")
            print(f"情感分數: {sentiment_score:.4f}, 情感傾向: {sentiment_level}\n")
    
    def run_full_training(self, json_dir, use_auto_labeling=True, sample_size=100):
        """執行完整的訓練流程"""
        # 步驟1: 提取評論數據
        reviews_data = self.extract_reviews_from_json(json_dir)
        
        # 步驟2: 標記數據
        if use_auto_labeling:
            # 自動根據評分標記
            positive_reviews, negative_reviews = self.auto_label_reviews(reviews_data)
        else:
            # 交互式手動標記
            positive_reviews, negative_reviews = self.interactive_labeling(reviews_data, sample_size)
        
        # 步驟3: 保存標記好的數據
        self.save_labeled_data(positive_reviews, negative_reviews)
        
        # 步驟4: 訓練模型
        self.train_sentiment_model()
        
        # 步驟5: 測試模型效果
        self.test_sentiment_model()
        
        return {
            "model_path": self.model_path,
            "positive_count": len(positive_reviews),
            "negative_count": len(negative_reviews)
        }
    
    def evaluate_model_accuracy(self, test_data):
        """評估模型準確率"""
        correct = 0
        total = len(test_data)
        
        for item in test_data:
            text = item['text']
            actual_sentiment = 'positive' if item['rating'] >= 4 else 'negative'
            
            s = SnowNLP(self.preprocess_text(text))
            predicted_sentiment = 'positive' if s.sentiments > 0.5 else 'negative'
            
            if actual_sentiment == predicted_sentiment:
                correct += 1
        
        accuracy = correct / total if total > 0 else 0
        print(f"模型準確率: {accuracy:.4f} ({correct}/{total})")
        return accuracy

# 如果直接執行，則運行示例訓練流程
if __name__ == "__main__":
    trainer = SentimentTrainer()
    
    # 設置訓練數據目錄
    json_dir = "/home/user/YunTech2025/schoolProject/xxSearchCrawler/output_comments"
    
    # 執行完整訓練流程
    result = trainer.run_full_training(json_dir, use_auto_labeling=True)
    
    print("\n" + "=" * 50)
    print(f"模型訓練完成！")
    print(f"模型保存路徑: {result['model_path']}")
    print(f"正面評論數量: {result['positive_count']}")
    print(f"負面評論數量: {result['negative_count']}")