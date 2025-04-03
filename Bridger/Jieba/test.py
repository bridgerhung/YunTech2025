import jieba
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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

# 方法 3：文本共現關係分析
def extract_co_occurrences(texts, window_size=2):
    co_occurrences = Counter()
    
    for text in texts:
        words = [w for w in jieba.lcut(text) if w not in stop_words and len(w) > 1]
        
        for i in range(len(words)):
            for j in range(i+1, min(i+window_size+1, len(words))):
                if words[i] != words[j]:  # 避免自我共現
                    # 按字母順序排序以避免重複計算
                    word_pair = tuple(sorted([words[i], words[j]]))
                    co_occurrences[word_pair] += 1
    
    return co_occurrences

co_occurrences = extract_co_occurrences(articles)
print("共現關係分析 (詞組):", co_occurrences.most_common(5))

# 方法 4：TextRank 演算法簡化版
def textrank_keywords(texts, top_n=5):
    # 建立詞彙表和詞向量
    unique_words = set()
    for text in texts:
        words = [w for w in jieba.lcut(text) if w not in stop_words and len(w) > 1]
        unique_words.update(words)
    
    word_to_idx = {word: i for i, word in enumerate(unique_words)}
    idx_to_word = {i: word for word, i in word_to_idx.items()}
    
    # 詞頻矩陣
    word_vectors = np.zeros((len(unique_words), len(texts)))
    
    for i, text in enumerate(texts):
        words = [w for w in jieba.lcut(text) if w not in stop_words and len(w) > 1]
        for word in words:
            word_vectors[word_to_idx[word], i] += 1
    
    # 計算詞語之間的相似度
    similarity_matrix = cosine_similarity(word_vectors)
    np.fill_diagonal(similarity_matrix, 0)  # 消除自相似
    
    # 計算每個詞的得分 (行求和)
    scores = similarity_matrix.sum(axis=1)
    
    # 獲取前 N 個關鍵詞
    top_indices = scores.argsort()[-top_n:][::-1]
    return [(idx_to_word[idx], scores[idx]) for idx in top_indices]

textrank_keywords_result = textrank_keywords(articles)
print("TextRank 關鍵詞:", textrank_keywords_result)