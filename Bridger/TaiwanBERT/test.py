from pymongo import MongoClient
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import jieba
from collections import Counter

# 連接到 MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ptt_3c']
collection = db['articles']

# 載入微調後的模型
model = AutoModelForSequenceClassification.from_pretrained("./fine_tuned_taiwanbert")
tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_taiwanbert")

# 假設多篇 PTT 文章
articles = [
    """
    [心得] iPhone 15 使用心得
    這款iPhone 15真的很棒，拍照效果很好，特別是夜景模式。
    但是價格有點高，電池續航力還可以，沒有特別突出。
    整體來說，還是值得購買的。
    """,
    """
    [評價] iPhone 15 開箱
    iPhone 15的拍照功能超強，夜景模式很棒。
    但價格真的太貴了，電池續航力普通。
    """,
]

# 情感分析與後處理
label_map = {0: "正面", 1: "負面", 2: "中性"}
stop_words = {'的', '了', '是', '在', '有', '和', '也', '都', '，', '。'}

def post_process_sentiment(sentence, predicted_sentiment):
    if "價格" in sentence and any(word in sentence for word in ["高", "貴"]):
        return "負面"
    if any(word in sentence for word in ["值得", "推薦"]):
        return "正面"
    return predicted_sentiment

# 處理並儲存數據
for article in articles:
    words = [word for word in jieba.cut(article) if word not in stop_words and len(word) > 1]
    word_counts = Counter(words)
    sentences = article.split('。')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    sentiment_results = []
    model.eval()
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=128)
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
        predicted_sentiment = label_map[predictions.item()]
        final_sentiment = post_process_sentiment(sentence, predicted_sentiment)
        sentiment_results.append({"sentence": sentence, "sentiment": final_sentiment})

    article_data = {
        "raw_text": article,
        "segmented_words": words,
        "word_counts": dict(word_counts),
        "sentences": sentiment_results,
        "product": "iPhone 15"
    }
    collection.insert_one(article_data)

# 生成總結
product = "iPhone 15"
articles = collection.find({"product": product})

total_word_counts = Counter()
sentiment_counts = {"正面": 0, "負面": 0, "中性": 0}
positive_keywords = Counter()
negative_keywords = Counter()

for article in articles:
    total_word_counts.update(article["word_counts"])
    for sentence in article["sentences"]:
        sentiment = sentence["sentiment"]
        sentiment_counts[sentiment] += 1
        sentence_text = sentence["sentence"]
        words = [word for word in jieba.cut(sentence_text) if word not in stop_words and len(word) > 1]
        if sentiment == "正面":
            positive_keywords.update(words)
        elif sentiment == "負面":
            negative_keywords.update(words)

total_sentences = sum(sentiment_counts.values())
positive_ratio = sentiment_counts["正面"] / total_sentences
negative_ratio = sentiment_counts["負面"] / total_sentences

if positive_ratio > 0.6:
    overall_sentiment = "大多數用戶對 iPhone 15 持正面評價"
elif negative_ratio > 0.6:
    overall_sentiment = "大多數用戶對 iPhone 15 持負面評價"
else:
    overall_sentiment = "用戶對 iPhone 15 的評價褒貶不一"

positive_summary = "正面評價中，用戶經常提到 " + "、".join([f"{word}（{count} 次）" for word, count in positive_keywords.most_common(3)])
negative_summary = "負面評價中，用戶經常提到 " + "、".join([f"{word}（{count} 次）" for word, count in negative_keywords.most_common(3)])

summary = f"{overall_sentiment}。\n{positive_summary}。\n{negative_summary}。"
print("總結:", summary)