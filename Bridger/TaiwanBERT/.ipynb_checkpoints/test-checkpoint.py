import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import json
import os

from transformers import (
    BertTokenizerFast,
    AutoModel,
)

# 載入模型
tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
model = AutoModel.from_pretrained('ckiplab/bert-base-chinese')

# 詞彙列表
words = [
    "值得", "偏貴", "適合", "唯一", "強大",
    "迅速", "有限", "突出", "日常", "還可以",
    "友善", "靈敏", "特別", "好用", "不錯",
    "便宜", "精美", "高級", "差", "難用"
]

# 獲取詞向量
inputs = tokenizer(words, return_tensors="pt", padding=True)
outputs = model(**inputs)
embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()

# 設定評估的 K 範圍
k_range = range(2, 8)  # 測試 2 到 7 群

# 1. 輪廓係數評估
silhouette_scores = []
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10)
    cluster_labels = kmeans.fit_predict(embeddings)
    silhouette_avg = silhouette_score(embeddings, cluster_labels)
    silhouette_scores.append(silhouette_avg)
    print(f"K={k}，輪廓係數={silhouette_avg:.4f}")

best_k_silhouette = k_range[np.argmax(silhouette_scores)]
print(f"\n根據輪廓係數，最佳的群數為: {best_k_silhouette}")

# 2. 肘部法則評估
inertias = []
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10)
    kmeans.fit(embeddings)
    inertias.append(kmeans.inertia_)
    print(f"K={k}，慣性值={kmeans.inertia_:.4f}")

# 視覺化結果
plt.figure(figsize=(12, 10))

# 輪廓係數圖
plt.subplot(2, 1, 1)
plt.plot(k_range, silhouette_scores, 'o-', color='blue')
plt.axvline(x=best_k_silhouette, color='r', linestyle='--')
plt.xlabel('群數 (K)')
plt.ylabel('輪廓係數')
plt.title('輪廓係數法尋找最佳群數')
plt.grid(True)

# 肘部法則圖
plt.subplot(2, 1, 2)
plt.plot(k_range, inertias, 'o-', color='green')
plt.xlabel('群數 (K)')
plt.ylabel('慣性值 (Inertia)')
plt.title('肘部法則尋找最佳群數')
plt.grid(True)

plt.tight_layout()
plt.savefig('kmeans_optimization.png')
print("\n優化結果圖已保存為 'kmeans_optimization.png'")

# 使用最佳 K 值進行最終分群
final_k = best_k_silhouette  # 以輪廓係數的結果為準
final_kmeans = KMeans(n_clusters=final_k, random_state=0, n_init=10)
final_labels = final_kmeans.fit_predict(embeddings)

# 輸出每個群的詞彙
clusters = {}
for i, (word, label) in enumerate(zip(words, final_labels)):
    if label not in clusters:
        clusters[label] = []
    clusters[label].append(word)

print(f"\n使用 K={final_k} 的分群結果:")
for label, cluster_words in clusters.items():
    print(f"群 {label}: {', '.join(cluster_words)}")

# 將每個群的詞彙保存為 JSON
cluster_json = {}
for label, cluster_words in clusters.items():
    cluster_json[f"cluster_{label}"] = cluster_words

with open('word_clusters.json', 'w', encoding='utf-8') as f:
    json.dump(cluster_json, f, ensure_ascii=False, indent=2)

print("\n分群結果已保存為 'word_clusters.json'")