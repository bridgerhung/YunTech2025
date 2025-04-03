import os
import json
from ckiptagger import WS, POS, NER, data_utils, construct_dictionary

# 設定正確的路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "data")

# 檢查數據是否存在
if not os.path.exists(data_dir) or not os.path.exists(os.path.join(data_dir, "embedding_character")):
    print("模型資料不存在，請先下載模型資料")
    exit()

# 初始化工具
print("正在載入模型...")
ws = WS(data_dir, disable_cuda=False)
pos = POS(data_dir, disable_cuda=False)
ner = NER(data_dir, disable_cuda=False)
print("模型載入完成")

def extract_words_by_pos(word_list, pos_list, pos_prefixes):
    """
    從斷詞和詞性標註結果中提取特定詞性的詞彙
    pos_prefixes: 要提取的詞性前綴列表，如 ['A', 'VH'] 表示形容詞和狀態不及物動詞
    """
    extracted_words = []
    
    for sentence_words, sentence_pos in zip(word_list, pos_list):
        for word, pos in zip(sentence_words, sentence_pos):
            # 檢查詞性是否匹配任一前綴
            if any(pos.startswith(prefix) for prefix in pos_prefixes):
                # 只提取長度大於1的詞
                if len(word) > 1:
                    extracted_words.append(word)
    
    # 移除重複詞彙
    unique_words = list(set(extracted_words))
    return unique_words

# 測試文本
test_text = """
[心得] iPhone 15 使用心得
這款iPhone 15真的很棒，拍照效果很好，特別是夜景模式。
但是價格有點高，電池續航力還可以，沒有特別突出。
整體來說，還是值得購買的。這支手機速度快、反應靈敏，非常適合日常使用。
相機功能強大，色彩表現自然，對焦迅速，是攝影愛好者的好選擇。
唯一的缺點就是價格偏貴，對於預算有限的人來說可能不太友善。
"""

# 斷詞和詞性標註
word_sentence_list = ws([test_text])
pos_sentence_list = pos(word_sentence_list)

# 1. 提取形容詞 (A)
adjectives = extract_words_by_pos(word_sentence_list, pos_sentence_list, ['A'])

# 2. 提取評價類詞彙（形容詞 A + 狀態動詞 VH + 部分動詞 VJ）
evaluation_words = extract_words_by_pos(word_sentence_list, pos_sentence_list, ['A', 'VH', 'VJ'])

# 3. 提取名詞 (N)
nouns = extract_words_by_pos(word_sentence_list, pos_sentence_list, ['N'])

# 輸出為簡單的詞彙列表 JSON
# 1. 形容詞
with open(os.path.join(current_dir, "adjectives.json"), "w", encoding="utf-8") as f:
    json.dump(adjectives, f, ensure_ascii=False, indent=2)
print(f"\n形容詞列表 JSON:")
print(json.dumps(adjectives, ensure_ascii=False))

# 2. 評價類詞彙
with open(os.path.join(current_dir, "evaluation_words.json"), "w", encoding="utf-8") as f:
    json.dump(evaluation_words, f, ensure_ascii=False, indent=2)
print(f"\n評價類詞彙列表 JSON:")
print(json.dumps(evaluation_words, ensure_ascii=False))

# 3. 名詞
with open(os.path.join(current_dir, "nouns.json"), "w", encoding="utf-8") as f:
    json.dump(nouns, f, ensure_ascii=False, indent=2)
print(f"\n名詞列表 JSON:")
print(json.dumps(nouns, ensure_ascii=False))

# 釋放模型資源
del ws
del pos
del ner
print("\n模型資源已釋放")