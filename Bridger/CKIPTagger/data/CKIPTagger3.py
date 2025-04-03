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

# 自定義詞典
word_to_weight = {
    "iPhone": 1,
    "iPhone 15": 2,  # 權重更高，會優先選擇這個
    "拍照效果": 1,
    "電池續航力": 1
}
dictionary = construct_dictionary(word_to_weight)

def analyze_text(text, use_dictionary=True):
    """分析單一文本"""
    if use_dictionary:
        word_sentence_list = ws([text], recommend_dictionary=dictionary)
    else:
        word_sentence_list = ws([text])
    
    pos_sentence_list = pos(word_sentence_list)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)
    
    return word_sentence_list, pos_sentence_list, entity_sentence_list

def convert_to_json(sentence, word_list, pos_list, entity_list):
    """將分析結果轉換為 JSON 格式"""
    words_with_pos = []
    for word, pos_tag in zip(word_list[0], pos_list[0]):
        words_with_pos.append({
            "word": word,
            "pos": pos_tag
        })
    
    entities = []
    for entity in sorted(entity_list[0]):
        start_idx, end_idx, entity_type, entity_text = entity
        entities.append({
            "start_index": start_idx,
            "end_index": end_idx,
            "type": entity_type,
            "text": entity_text
        })
    
    result = {
        "sentence": sentence,
        "segments": words_with_pos,
        "entities": entities
    }
    
    return result

def save_to_json(data, filename):
    """儲存 JSON 結果到檔案"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"結果已儲存至 {filename}")

# 測試分析並轉換為 JSON
test_text = """
[心得] iPhone 15 使用心得
這款iPhone 15真的很棒，拍照效果很好，特別是夜景模式。
但是價格有點高，電池續航力還可以，沒有特別突出。
整體來說，還是值得購買的。
"""

# 分析文本
word_sentence_list, pos_sentence_list, entity_sentence_list = analyze_text(test_text, use_dictionary=True)

# 將結果轉換為 JSON
result_json = convert_to_json(test_text, word_sentence_list, pos_sentence_list, entity_sentence_list)

# 保存 JSON 結果
save_to_json(result_json, os.path.join(current_dir, "analysis_result.json"))

# 印出 JSON 範例
print("\nJSON 結果範例:")
print(json.dumps(result_json, ensure_ascii=False, indent=2))

# 釋放模型資源
del ws
del pos
del ner
print("模型資源已釋放")