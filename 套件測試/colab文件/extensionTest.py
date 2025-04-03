import jieba
import jieba.analyse
from collections import Counter, defaultdict
import itertools
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from google import genai
#from google.cloud import aiplatform as genai

# 讀取文件
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# 提取關鍵字
def extract_keywords(text, topk=25, dict_path=None, stop_path=None):
    if dict_path:
        jieba.set_dictionary(dict_path)
    if stop_path:
        jieba.analyse.set_stop_words(stop_path)
    return jieba.analyse.extract_tags(text, topK=topk)

# 計算共現關鍵字的函數
def calculate_co_occurrence(sentences, tags, window_size=5):
    co_occurrence = defaultdict(int)
    for sent in sentences:
        for word1, word2 in itertools.combinations(sent, 2):
            if word1 in tags and word2 in tags:
                co_occurrence[(word1, word2)] += 1
    return co_occurrence

# 生成詞雲的函數
def generate_wordcloud(freq, mask_path, font_path, output_path="wordcloud.png"):
    mask = np.array(Image.open(mask_path))
    wc = WordCloud(width=800, height=400, mask=mask, font_path=font_path, background_color="white").generate_from_frequencies(freq)
    image_colors = ImageColorGenerator(mask)
    wc.recolor(color_func=image_colors)
    plt.figure(figsize=(5, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(output_path)
    plt.show()

# 處理文本並生成關鍵字
text = read_file("/home/user/YunTech2025/套件測試/colab文件/測試文案.txt")
tags = extract_keywords(text, dict_path="/home/user/YunTech2025/套件測試/colab文件/dict (1).txt", stop_path="/home/user/YunTech2025/套件測試/colab文件/stopwords (1).txt")

# 將文本切割成句子
sentences = [list(jieba.cut(sent)) for sent in text.split("\n")]
co_occurrence = calculate_co_occurrence(sentences, tags)

# 輸出共現分析結果
print('\n================共現分析=================')
print(sorted(co_occurrence.items(), key=lambda x: x[1], reverse=True)[:10])

# 根據共現頻次過濾句子
list_selected = [''.join(s) for s in sentences if any(c[0][0] in ''.join(s) and c[0][1] in ''.join(s) for c in co_occurrence.items())]

# 如果需要進一步提高共現強度，可以根據每個關鍵詞對的共現次數來選擇句子
list_selected_sorted = sorted(list_selected, key=lambda x: sum(co_occurrence.get((tag1, tag2), 0) for tag1 in tags for tag2 in tags if tag1 in x and tag2 in x), reverse=True)

# 計算高頻關鍵字
freq = {ele: Counter(jieba.lcut(text))[ele] for ele in tags}

print('\n==================高詞頻關鍵字==================')
print(tags)

# 使用 Gemini API 生成摘要
client = genai.Client(api_key="AIzaSyBWBS1bgw7ojaCCsTqHXrnF27pcknqoXjo")
print('\n==========電腦太爛所以丟給gemini api來摘要==========')

# 只傳遞選擇出的句子生成摘要
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["依照我給你的list，給我一段純文字的結論，不用其他格式，", list_selected_sorted]  # 僅選擇前5個共現強的句子
)
print(response.text)
print(len(list_selected))

# 生成詞雲
generate_wordcloud(freq, "/home/user/YunTech2025/套件測試/colab文件/goblin.jpg", "/home/user/YunTech2025/套件測試/colab文件/Iansui/Iansui-Regular.ttf")
