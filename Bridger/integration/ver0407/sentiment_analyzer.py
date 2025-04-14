from snownlp import SnowNLP
import jieba
from collections import defaultdict
import pandas as pd
import os
import importlib
import opencc
import re

class SentimentAnalyzer:
    def __init__(self, custom_model_path=None):
        # 繁簡轉換設定
        self.converter = opencc.OpenCC('tw2sp')
        
        # 電商評論中常見的情感指示詞及其權重 - 增強負面詞彙的權重
        self.sentiment_indicators = {
            # 正面評價詞
            "好用": 0.9, "優質": 0.9, "推薦": 0.9, "滿意": 0.85, "方便": 0.8, 
            "簡單": 0.7, "容易": 0.7, "不錯": 0.7, "快速": 0.7, "穩定": 0.8,
            "耐用": 0.8, "實用": 0.7, "划算": 0.7, "便宜": 0.6, "超值": 0.8,
            "高效": 0.8, "優惠": 0.6, "喜歡": 0.8, "讚": 0.9, "推": 0.8,
            "正品": 0.7, "優": 0.7, "佳": 0.7, "值得": 0.7, "超好用": 0.95,
            "即插即用": 0.8,
            
            # 負面評價詞 - 調高權重，增加針對簡體中文、內地貨等特定詞彙的負面權重
            "差": -0.9, "爛": -0.95, "失望": -0.9, "退貨": -0.8, "不推薦": -0.9,
            "問題": -0.7, "壞了": -0.85, "不良": -0.8, "當機": -0.9, "缺點": -0.7,
            "慢": -0.75, "卡": -0.7, "不穩定": -0.8, "漏電": -0.95, "資安": -0.95,
            "太差": -0.95, "難用": -0.85, "不好用": -0.85, "不順": -0.7, 
            # 新增電商產品常見負面詞彙
            "效能差": -0.9, "變慢": -0.85, "不能": -0.7, "有限": -0.6, "限制": -0.7,
            "不夠": -0.7, "不足": -0.7, "降低": -0.6, "低於": -0.7, "弱": -0.7,
            # 新增特定產地/語言相關負面詞彙
            "簡體": -0.7, "內地貨": -0.8, "中國品牌": -0.9, "中國製": -0.7, "過大": -0.6, 
            "無法傳": -0.8, "不是很優": -0.9, "不優": -0.85, "陸製": -0.7, "大陸貨": -0.75,
            "需注意": -0.85, "注意": -0.7
        }

        # 品牌關聯詞彙
        self.brand_indicators = {
            "TP-Link": {"中國品牌": -0.9, "資安問題": -0.95, "資安": -0.9},
            "華為": {"中國品牌": -0.9, "資安問題": -0.95, "資安": -0.9},
            "小米": {"中國品牌": -0.9, "資安問題": -0.95, "資安": -0.9},
            "聯想": {"中國品牌": -0.8, "資安問題": -0.95, "資安": -0.9},
            "海爾": {"中國品牌": -0.8, "資安問題": -0.95, "資安": -0.9},
        }
        
        # 比較詞組合檢測，特別是對比句
        self.comparison_patterns = [
            (r'比.+差', -0.8),           # 比...差
            (r'沒有.+好', -0.7),         # 沒有...好
            (r'不如.+', -0.7),           # 不如...
            (r'低於.+', -0.7),           # 低於...
            (r'不能.+', -0.7),           # 不能...
            (r'只能.+', -0.6),           # 只能...
            (r'太.+了', -0.7),           # 太...了
            (r'無法.+', -0.8),           # 無法...
            (r'不是很.+', -0.75),        # 不是很...
            (r'需注意.+', -0.85),        # 需注意...
            (r'注意.+問題', -0.9)        # 注意...問題
        ]
        
        # 特殊句式模式 - 新增檢測雙面評價的模式
        self.special_patterns = [
            # 格式: (模式, 正面部分權重, 負面部分權重)
            (r'(.+)，但是(.+)', 0.3, 0.7),   # 前半句正面，後半句負面且權重較大
            (r'(.+)，不過(.+)', 0.3, 0.7),   # 前半句正面，後半句負面且權重較大
            (r'(.+)，可是(.+)', 0.3, 0.7),   # 前半句正面，後半句負面且權重較大
            (r'(.+)，就是(.+)', 0.2, 0.8),   # "就是"後面通常是強調缺點
            (r'(.+)，唯(.+)', 0.2, 0.8),     # "唯"後面通常是強調缺點
            (r'(.+)，需(.+)', 0.2, 0.8)      # "需"後面通常是強調缺點或注意事項
        ]
        
        # 如果提供了自訂模型路徑，則嘗試載入自訂模型
        self.custom_model_used = False
        if custom_model_path and os.path.exists(custom_model_path):
            try:
                # 指定自訂情感模型的路徑
                from snownlp import sentiment
                sentiment.path = custom_model_path
                # 重新載入情感模型
                importlib.reload(sentiment)
                self.custom_model_used = True
                print(f"已載入自訂情感分析模型: {custom_model_path}")
            except Exception as e:
                print(f"載入自訂情感模型失敗: {str(e)}")
        
    def preprocess_text(self, text):
        """預處理文本，轉為簡體中文以提高分析準確性"""
        if not text:
            return ""
            
        # 清理文本
        text = re.sub(r'<.*?>', '', text)  # 移除HTML標籤
        
        # 繁體轉簡體（SnowNLP對簡體中文效果較好）
        text = self.converter.convert(text)
        return text.strip()
    
    def check_comparison_patterns(self, text):
        """檢查文本是否包含比較句式"""
        matched_patterns = []
        for pattern, score in self.comparison_patterns:
            if re.search(pattern, text):
                matched_patterns.append((pattern, score))
        return matched_patterns

    def check_special_patterns(self, text):
        """檢查包含轉折的複合句"""
        for pattern, pos_weight, neg_weight in self.special_patterns:
            match = re.search(pattern, text)
            if match:
                return (match.group(1), match.group(2), pos_weight, neg_weight)
        return None
    
    def check_brand_security_issues(self, text):
        """檢查是否包含品牌資安問題相關內容"""
        matched_indicators = []
        
        # 檢查是否同時出現品牌和資安相關詞彙
        for brand, indicators in self.brand_indicators.items():
            if brand.lower() in text.lower():
                for keyword, weight in indicators.items():
                    if keyword.lower() in text.lower():
                        matched_indicators.append((f"{brand}:{keyword}", weight))
        
        return matched_indicators
    
    def adjust_sentiment_with_keywords(self, text, original_score):
        """根據情感指示詞調整情感分數"""
        words = jieba.lcut(text.lower())
        score_adjustment = 0
        matched_indicators = []
        
        # 檢查品牌資安問題
        brand_security_issues = self.check_brand_security_issues(text)
        if brand_security_issues:
            for issue, weight in brand_security_issues:
                score_adjustment += weight * 2  # 加倍權重，因為這是特別重要的因素
                matched_indicators.append((issue, weight * 2))
            
            # 品牌資安問題特別重要，直接影響評分
            if original_score > 0.5:  # 原本是正面評價
                adjusted_score = max(0.1, original_score * 0.2)  # 強制降到負面
                return adjusted_score, matched_indicators
        
        # 檢查是否包含特殊句式（如轉折句）
        special_match = self.check_special_patterns(text)
        if special_match:
            # 拆分句子成正面部分和負面部分
            positive_part, negative_part, pos_weight, neg_weight = special_match
            
            # 正面部分的情感分析
            pos_score = SnowNLP(self.preprocess_text(positive_part)).sentiments
            
            # 負面部分的情感分析
            neg_score = SnowNLP(self.preprocess_text(negative_part)).sentiments
            
            # 加權平均
            adjusted_score = pos_score * pos_weight + neg_score * neg_weight
            matched_indicators.append(("複合句式", neg_weight - pos_weight))
            
            return adjusted_score, matched_indicators
        
        # 檢查是否包含比較句式
        comparison_matches = self.check_comparison_patterns(text)
        if comparison_matches:
            for pattern, score in comparison_matches:
                score_adjustment += score
                matched_indicators.append((f"比較句:{pattern}", score))
        
        # 特殊處理：超好用、操作簡單相關評論
        if "超好用" in text or ("好用" in text and "簡單" in text):
            score_adjustment += 1.0  # 強化正面評價
            matched_indicators.append(("強化好評", 1.0))
        
        # 檢查單個詞彙
        for word in words:
            if word in self.sentiment_indicators:
                weight = self.sentiment_indicators[word]
                score_adjustment += weight
                matched_indicators.append((word, weight))
        
        # 調整分數，但保持在0-1範圍內
        if matched_indicators:
            # 根據找到的指示詞數量計算調整幅度
            adjustment_strength = min(0.6, 0.25 * len(matched_indicators))  # 增加最大調整幅度
            
            # 應用調整
            if score_adjustment > 0:
                adjusted_score = original_score * (1 - adjustment_strength) + adjustment_strength * 0.9
            elif score_adjustment < 0:
                adjusted_score = original_score * (1 - adjustment_strength) + adjustment_strength * 0.1
            else:
                adjusted_score = original_score
                
            # 確保分數在0-1範圍內
            adjusted_score = max(0.0, min(1.0, adjusted_score))
        else:
            adjusted_score = original_score
            
        return adjusted_score, matched_indicators
        
    def analyze_sentiment(self, sentences):
        """分析一系列句子的情感傾向並返回統計結果"""
        if not sentences:
            return {
                "score": 0,
                "positive_percent": 0,
                "sentiment_level": "無資料",
                "sentence_count": 0,
                "sentence_details": []
            }
            
        sentiment_scores = []
        sentence_details = []
        
        for sentence in sentences:
            if not sentence or sentence.isspace():
                continue
                
            # 預處理文本（繁轉簡）
            processed_text = self.preprocess_text(sentence)
            
            # 使用 SnowNLP 分析情感
            s = SnowNLP(processed_text)
            original_score = s.sentiments
            
            # 根據電商領域詞彙調整情感分數
            adjusted_score, indicators = self.adjust_sentiment_with_keywords(processed_text, original_score)
            
            sentiment_scores.append(adjusted_score)
            sentence_details.append({
                "text": sentence,
                "processed_text": processed_text,
                "original_score": original_score,
                "adjusted_score": adjusted_score,
                "matched_indicators": indicators,
                "level": self._get_sentiment_level(adjusted_score)
            })
        
        # 計算平均分數和百分比
        if sentiment_scores:
            avg_score = sum(sentiment_scores) / len(sentiment_scores)
            positive_percent = avg_score * 100
        else:
            avg_score = 0
            positive_percent = 0
        
        return {
            "score": avg_score,
            "positive_percent": positive_percent,
            "sentiment_level": self._get_sentiment_level(avg_score),
            "sentence_count": len(sentiment_scores),
            "sentence_details": sentence_details,
            "custom_model_used": self.custom_model_used
        }
    
    def _get_sentiment_level(self, score):
        """根據情感分數返回情感級別 - 調整閾值使其更符合電商評論特性"""
        if score > 0.7:  # 提高判定為正面評價的門檻
            return "正面"
        elif score > 0.4:  # 擴大中性評價的範圍
            return "中性"
        elif score > 0.2:  # 略微負面的評論
            return "負面"
        else:  # 明顯負面的評論
            return "非常負面"
            
    def analyze_text_block(self, text):
        """分析整個文本塊的情感傾向"""
        sentences = text.split('\n')
        return self.analyze_sentiment([s for s in sentences if s.strip()])
    
    def print_sentence_sentiments(self, sentences):
        """列出每個句子的情感傾向並輸出"""
        result = self.analyze_sentiment(sentences)
        
        print("\n" + "="*20 + " 情感分析結果 " + "="*20)
        print(f"整體情感傾向: {result['sentiment_level']} (正面程度: {result['positive_percent']:.2f}%)")
        print(f"分析句子數量: {result['sentence_count']}")
        if self.custom_model_used:
            print("使用自訂訓練模型分析")
        print("-"*55)
        print("各句評論情感分析:")
        
        sentence_data = []
        for i, detail in enumerate(result['sentence_details'], 1):
            text = detail['text'] if len(detail['text']) <= 30 else detail['text'][:27] + "..."
            
            # 顯示原始分數和調整後的分數
            sentiment = f"{detail['level']} (調整前:{detail['original_score']:.2f}, 調整後:{detail['adjusted_score']:.2f})"
            
            # 如果有匹配的情感指示詞，顯示出來
            indicators = []
            if 'matched_indicators' in detail and detail['matched_indicators']:
                indicators = [f"{word}({weight:+.1f})" for word, weight in detail['matched_indicators']]
            
            if indicators:
                print(f"{i}. {text} - {sentiment} 關鍵詞:{', '.join(indicators)}")
            else:
                print(f"{i}. {text} - {sentiment}")
                
            sentence_data.append({
                "序號": i,
                "評論": detail['text'],
                "原始情感分數": detail['original_score'],
                "調整後情感分數": detail['adjusted_score'],
                "情感傾向": detail['level'],
                "情感指示詞": "|".join(indicators) if indicators else ""
            })
        
        print("="*55 + "\n")
        return pd.DataFrame(sentence_data)
    
    def get_sentiment_dataframe(self, sentences):
        """返回情感分析結果的 DataFrame 格式"""
        result = self.analyze_sentiment(sentences)
        sentence_data = []
        
        for i, detail in enumerate(result['sentence_details'], 1):
            indicators = []
            if 'matched_indicators' in detail and detail['matched_indicators']:
                indicators = [f"{word}({weight:+.1f})" for word, weight in detail['matched_indicators']]
                
            sentence_data.append({
                "序號": i,
                "評論": detail['text'],
                "原始情感分數": detail['original_score'],
                "調整後情感分數": detail['adjusted_score'],
                "情感傾向": detail['level'],
                "情感指示詞": "|".join(indicators) if indicators else ""
            })
        
        return pd.DataFrame(sentence_data)