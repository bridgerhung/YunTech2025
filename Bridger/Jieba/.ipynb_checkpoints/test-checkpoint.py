import jieba
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from keybert import KeyBERT

# 假設 PTT 文章
articles = [
    "這款iPhone 15真的很棒，拍照效果很好，特別是夜景模式。",
    "iPhone 15的價格有點高，電池續航力還可以，沒有特別突出。",
    "整體來說，iPhone 15還是值得購買的，螢幕顯示很清晰。",
]

# 自定義停用詞
stop_words = {'的', '了', '是', '在', '有', '和', '也', '都', '，', '。'}

# 方法 1：Jieba 詞頻統計
word_counts = Counter()
for article in articles:
    words = jieba.cut(article)
    words = [word for word in words if word not in stop_words and len(word) > 1]
    word_counts.update(words)
print("Jieba 詞頻統計:", word_counts.most_common(5))

# 方法 2：TF-IDF 關鍵詞提取
def tokenize(text):
    words = jieba.cut(text)
    return " ".join([word for word in words if word not in stop_words and len(word) > 1])

tokenized_articles = [tokenize(article) for article in articles]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(tokenized_articles)
feature_names = vectorizer.get_feature_names_out()
tfidf_scores = tfidf_matrix.toarray()
word_tfidf = {word: tfidf_scores[:, i].mean() for i, word in enumerate(feature_names)}
sorted_word_tfidf = sorted(word_tfidf.items(), key=lambda x: x[1], reverse=True)
print("TF-IDF 關鍵詞:", sorted_word_tfidf[:5])

# 方法 3：KeyBERT 關鍵詞提取
kw_model = KeyBERT()
combined_text = " ".join(articles)
tokenized_text = " ".join([word for word in jieba.cut(combined_text) if word not in stop_words and len(word) > 1])
keywords = kw_model.extract_keywords(tokenized_text, keyphrase_ngram_range=(1, 2), top_n=5)
keyword_counts = Counter()
for keyword, score in keywords:
    keyword_counts[keyword] = sum(article.count(keyword) for article in articles)
print("KeyBERT 關鍵詞與次數:", keyword_counts.most_common(5))