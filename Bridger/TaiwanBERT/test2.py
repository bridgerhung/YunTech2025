# !pip install --upgrade transformers accelerate
#  pip install tf-keras

from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch
from torch.utils.data import Dataset
import os
from pymongo import MongoClient
import jieba
from collections import Counter

# 確保儲存目錄存在
save_dir = "./fine_tuned_taiwanbert"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 定義數據
data = [
    ("這款iPhone 15真的很棒，拍照效果很好，特別是夜景模式。", "正面"),
    ("但是價格有點高，電池續航力還可以，沒有特別突出。", "負面"),
    ("整體來說，還是值得購買的。", "正面"),
    ("iPhone 15的螢幕顯示很清晰，設計很漂亮。", "正面"),
    ("電池續航力真的不行，用一天就沒電了。", "負面"),
    ("價格太貴了，性價比不高。", "負面"),
    ("這手機還可以，沒有特別驚艷。", "中性"),
]

# 載入分詞器和模型
tokenizer = AutoTokenizer.from_pretrained("ckiplab/bert-base-chinese")
model = AutoModelForSequenceClassification.from_pretrained("ckiplab/bert-base-chinese", num_labels=3)

# 情感標籤映射
label_map = {"正面": 0, "負面": 1, "中性": 2}

# 自定義數據集
class SentimentDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=128, return_tensors="pt")

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

# 準備數據
texts = [d[0] for d in data]
labels = [label_map[d[1]] for d in data]
dataset = SentimentDataset(texts, labels)

# 設置訓練參數
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
)

# 初始化 Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# 開始訓練
trainer.train()

# 儲存模型
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
print(f"模型已儲存到 {save_dir}")

# 連接到 MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ptt_3c']
collection = db['articles']

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