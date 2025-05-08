#!/usr/bin/env python3
import os
import sys
import subprocess

# 使用命令行直接調用llama.cpp，最簡單高效的方法

# 檢查llama.cpp執行檔
executable = '/home/user/YunTech2025/llama.cpp/build/bin/llama-cli'
if not os.path.exists(executable):
    executable = '/home/user/YunTech2025/llama.cpp/build/bin/main'
    if not os.path.exists(executable):
        print("無法找到llama.cpp執行檔，請確認路徑")
        sys.exit(1)

# 構建指令
model_path = "/home/user/YunTech2025/llama.cpp/models/Qwen3-0.6B.gguf"
# 在原始提示詞後加上 /no_think 來關閉思考功能
prompt = "請使用繁體中文自我介紹，並說明你是誰、你的能力、以及你能做什麼。/no_think"

# 最簡化的命令參數，以確保兼容性
command = [
    executable,
    "-m", model_path,
    "-p", prompt,
    "-n", "1024",
    "--temp", "0.7",
    "--color"
]

print("執行命令：", " ".join(command))
print("\n開始生成回應...\n")

# 直接執行，將輸出實時傳送到標準輸出，不拋轉為字串處理
subprocess.run(command)