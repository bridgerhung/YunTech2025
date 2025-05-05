from transformers import pipeline

# 載入 BART 總結模型
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# 從檔案讀取評論
with open("comments.txt", "r", encoding="utf-8") as f:
    comments = f.readlines()

# 合併評論
text = "\n".join(comments)

# 分段總結（BART 上下文長度限制為 1024 token）
def summarize_chunk(chunk):
    return summarizer(chunk, max_length=50, min_length=10, do_sample=False)[0]["summary_text"]

# 分段處理
chunk_size = 500  # 每段約 500 字
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
sub_summaries = [summarize_chunk(chunk) for chunk in chunks]

# 合併最終總結
final_text = "\n".join(sub_summaries)
final_summary = summarizer(final_text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
print(final_summary)

# 構建評論內容
comments_text = "\n".join(comments)

# 構建提示
prompt = (
    "你是一個繁體中文評論總結專家，請將以下評論濃縮為一段100字以內的摘要，重點突出主要意見（例如產品優缺點、用戶情感）並保持中立客觀。\n\n"
    f"評論：\n{comments_text}\n\n總結：\n"
)

# 生成總結
outputs = pipe(
    prompt,
    max_new_tokens=128,
    do_sample=True,
    temperature=0.7,
    top_k=50,
    top_p=0.95
)
print(outputs[0]["generated_text"])