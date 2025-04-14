from decodeJson import decodeJson
from kw import keywordGetter
from summerize import summerizer
from sentiment_analyzer import SentimentAnalyzer
import jieba
from cloud import wordCloudGenerator
import pandas as pd
import os
import matplotlib.pyplot as plt

def search(decoder, keyword, include_momo=True):
    """搜尋評論，包含 momo 資料集"""
    filtered_df = decoder.search_reviews(keyword)
    
    # 顯示平台統計資訊
    platform_stats = decoder.get_platform_stats()
    print("\n" + "="*20 + " 平台評論統計 " + "="*20)
    for platform, count in platform_stats.items():
        print(f"{platform}: {count} 則評論")
    print("="*55 + "\n")
    
    return filtered_df

def getKeyword(kwGetter, inputResult, modelMode):
    """提取關鍵詞"""
    return kwGetter.extract_keywords(text=inputResult, modelMode=modelMode)

def cloud(kwGetter, decoder, output_path=None):
    """生成文字雲"""
    text = decoder.makeSentence()
    if not text or text.isspace():
        print("沒有足夠的評論來生成文字雲")
        return
        
    commentKeys = getKeyword(kwGetter, text, False)
    fq = kwGetter.getFreq(text, commentKeys)
    
    # 如果沒有足夠的關鍵詞
    if not fq:
        print("沒有提取到有效的關鍵詞，無法生成文字雲")
        return
    
    cloudmaker = wordCloudGenerator()
    
    # 確保路徑存在
    mask_path = 'meatballSpaghetii/integration/resource/goblin.jpg'
    font_path = 'meatballSpaghetii/integration/resource/Iansui/Iansui-Regular.ttf'
    
    if not os.path.exists(mask_path):
        print(f"遮罩文件不存在: {mask_path}")
        mask_path = None
    
    if not os.path.exists(font_path):
        print(f"字體文件不存在: {font_path}")
        font_path = None
    
    # 生成文字雲
    cloudmaker.generate_wordcloud(fq, mask_path=mask_path, font_path=font_path, output_path=output_path)
    print("文字雲生成完成")

def analyze_sentiment(text_list, custom_model_path='model_training/sentiment.marshal'):
    """分析情感並返回結果 DataFrame"""
    # 過濾掉空評論或只包含冒號(:)的評論
    filtered_sentences = [s for s in text_list if s and len(s.strip()) > 1 and not s.strip().startswith(':')]
    
    # 只有當有非空評論時才進行情感分析
    if filtered_sentences:
        # 使用 SnowNLP 進行情感分析
        sentiment_analyzer = SentimentAnalyzer(custom_model_path=custom_model_path)
        sentence_df = sentiment_analyzer.print_sentence_sentiments(filtered_sentences)
        return sentence_df
    else:
        print("\n" + "="*20 + " 情感分析結果 " + "="*20)
        print("無有效評論可進行情感分析")
        print("="*55 + "\n")
        return pd.DataFrame(columns=['sentence', 'sentiment'])

def summerize_reviews(kwGetter, decoder, key):
    """摘要評論並進行情感分析"""
    text = decoder.makeSentence()
    if not text or text.isspace():
        print("沒有足夠的評論來進行摘要")
        return
    
    commentKeys = getKeyword(kwGetter, text, False)
    
    try:
        sentences = [list(jieba.cut(sent)) for sent in text.split("\n") if sent.strip()]
        co_occurrence = kwGetter.calculate_co_occurrence(sentences, commentKeys)
        
        # 篩選包含共現詞對的句子
        list_selected = []
        for s in sentences:
            sentence = ''.join(s)
            for c in co_occurrence.items():
                if c[0][0] in sentence and c[0][1] in sentence:
                    list_selected.append(sentence)
                    break
        
        # 過濾掉空評論或只包含冒號(:)的評論
        filtered_sentences = [s for s in list_selected if s and len(s.strip()) > 1 and not s.strip().startswith(':')]
        
        # 情感分析
        sentiment_df = analyze_sentiment(filtered_sentences)
        
        # 將評論按情感劃分
        if not sentiment_df.empty:
            positive_reviews = sentiment_df[sentiment_df['sentiment'] > 0.6]['sentence'].tolist()
            negative_reviews = sentiment_df[sentiment_df['sentiment'] < 0.4]['sentence'].tolist()
            neutral_reviews = sentiment_df[(sentiment_df['sentiment'] >= 0.4) & 
                                       (sentiment_df['sentiment'] <= 0.6)]['sentence'].tolist()
            
            print(f"\n正面評論數量: {len(positive_reviews)}")
            print(f"負面評論數量: {len(negative_reviews)}")
            print(f"中性評論數量: {len(neutral_reviews)}")
            
            # 輸出情感分布
            plot_sentiment_distribution(sentiment_df)
        
        # 原有的 Gemini API 摘要功能
        summer = summerizer()
        summer.sum(filtered_sentences, key)
        
    except Exception as e:
        print(f"處理評論時發生錯誤: {str(e)}")

def plot_sentiment_distribution(sentiment_df):
    """繪製情感分布圖"""
    if sentiment_df.empty:
        return
    
    try:
        plt.figure(figsize=(10, 6))
        plt.hist(sentiment_df['sentiment'], bins=20, color='skyblue', edgecolor='black')
        plt.axvline(x=0.5, color='red', linestyle='--', alpha=0.7)
        plt.title('評論情感分佈')
        plt.xlabel('情感分數 (0=負面, 1=正面)')
        plt.ylabel('評論數量')
        plt.grid(alpha=0.3)
        
        # 計算平均情感分數
        avg_sentiment = sentiment_df['sentiment'].mean()
        plt.axvline(x=avg_sentiment, color='green', linestyle='-', alpha=0.7)
        plt.text(avg_sentiment, plt.ylim()[1]*0.9, f'平均: {avg_sentiment:.2f}', 
                 horizontalalignment='center', color='darkgreen')
        
        plt.savefig('sentiment_distribution.png')
        plt.close()
        print("已生成情感分布圖 sentiment_distribution.png")
        
    except Exception as e:
        print(f"繪製情感分布圖時發生錯誤: {str(e)}")

def main():
    """主程式流程"""
    decoder = decodeJson()
    kwGetter = keywordGetter()
    
    # 用戶輸入
    text = input("請輸入你想要搜索的產品關鍵字: ")
    include_momo = input("是否包含 momo 資料集? (y/n, 預設為 y): ").lower() != 'n'
    
    # 提取關鍵字
    key = getKeyword(kwGetter, text, True)
    print(f"提取的關鍵字: {', '.join(key)}")
    
    print("="*50)
    
    # 搜尋評論
    search(decoder, key, include_momo)
    
    # 生成摘要和情感分析
    summerize_reviews(kwGetter, decoder, key)
    
    # 生成文字雲
    cloud_option = input("是否生成文字雲? (y/n, 預設為 y): ").lower() != 'n'
    if cloud_option:
        output_path = f"wordcloud_{'-'.join(key)}.png"
        cloud(kwGetter, decoder, output_path)

if __name__ == "__main__":
    main()