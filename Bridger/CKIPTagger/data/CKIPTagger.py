# conda create -n ckiptagger Python 3.9.21
# For 耀翔 conda activate ckiptagger
# For 耀翔 select interpreter ckiptagger
# pip install ckiptagger tensorflow==2.10.0 gdown
# For 耀翔 conda deactivate 退出環境

# pip install numpy 1.22.4
# pip install protobuf==3.19.4
# pip install keras==2.10.0

import os
import json
from ckiptagger import WS, POS, NER, data_utils , construct_dictionary
# os: 用於處理文件路徑
# WS: 用於斷詞 (Word Segmentation)
# POS: 用於詞性標註 (Part-of-Speech Tagging)
# NER: 用於命名實體識別 (Named Entity Recognition)
# data_utils: 用於下載模型資料
# construct_dictionary: 用於構建自定義字典

# 設定正確的路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # Go up one level
data_dir = os.path.join(current_dir, "data")

# 檢查數據是否存在，如果不存在則下載
if not os.path.exists(data_dir) or not os.path.exists(os.path.join(data_dir, "embedding_character")):
    print("正在下載 CKIP Tagger 模型資料 (約需要 2GB 空間)...")
    os.makedirs(data_dir, exist_ok=True)
    data_utils.download_data(data_dir)
    print("模型數據下載完成!")

# 初始化工具 - 使用完整路徑
# ws = WS(data_dir, disable_cuda=False)
# pos = POS(data_dir, disable_cuda=False)
# ner = NER(data_dir, disable_cuda=False)
# Initialize CKIPTagger tools with CUDA disabled
ws = WS(data_dir, disable_cuda=True)
pos = POS(data_dir, disable_cuda=True)
ner = NER(data_dir, disable_cuda=True)
# ws: 用於斷詞
# pos: 用於詞性標註
# ner: 用於命名實體識別

word_to_weight = {
    "iPhone": 1,
    "": 1,
    "來亂的": "的",
}
dictionary = construct_dictionary(word_to_weight)
print(dictionary)
# 這段程式碼創建了一個自定義詞典，用於幫助系統更好地識別某些特定的詞彙:

# 字典中的每個鍵是希望系統識別的詞
# 每個值是該詞的權重，權重越大，系統越傾向於將文本切分為這個詞

# Run WS-POS-NER pipeline
sentence_list = [
        """
[心得] iPhone 15 使用心得
這款iPhone 15真的很棒，拍照效果很好，特別是夜景模式。
但是價格有點高，電池續航力還可以，沒有特別突出。
整體來說，還是值得購買的。
""",
]
word_sentence_list = ws(sentence_list)
# word_sentence_list = ws(sentence_list, sentence_segmentation=True)
# word_sentence_list = ws(sentence_list, recommend_dictionary=dictionary)
# word_sentence_list = ws(sentence_list, coerce_dictionary=dictionary)
pos_sentence_list = pos(word_sentence_list)
entity_sentence_list = ner(word_sentence_list, pos_sentence_list)
# 定義了一個測試句子列表
# 調用 ws 進行斷詞
# 調用 pos 進行詞性標註
# 調用 ner 進行命名實體識別

# Release model
del ws
del pos
del ner

# Show results
def print_word_pos_sentence(word_sentence, pos_sentence):
    assert len(word_sentence) == len(pos_sentence)
    for word, pos in zip(word_sentence, pos_sentence):
        print(f"{word}({pos})", end="\u3000")
    print()
    return

for i, sentence in enumerate(sentence_list):
    print()
    print(f"'{sentence}'")
    print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])
    for entity in sorted(entity_sentence_list[i]):
        print(entity)
# 斷詞 (WS): 將中文句子分割成有意義的詞語，這對於中文處理非常重要，因為中文沒有明確的詞語分界

# 詞性標註 (POS): 標註每個詞的詞性，如名詞、動詞、形容詞等

# 命名實體識別 (NER): 識別文本中的特定類別實體，如人名、地名、組織名等

# 自定義詞典: 提高特定領域詞彙的識別準確率
