from decodeJson import decodeJson
from kw import keywordGetter
from summerize import summerizer
from sentiment_analyzer import SentimentAnalyzer
import jieba
from cloud import wordCloudGenerator

def search(decoder, keyword):
    filtered_df = decoder.search_reviews(keyword)

def getKeyword(kwGetter, inputResult, modelMode):
    return kwGetter.extract_keywords(text=inputResult, modelMode=modelMode)

def cloud(kwGetter, decoder):
    text = decoder.makeSentence()
    commentKeys = getKeyword(kwGetter, text, False)
    fq = kwGetter.getFreq(text, commentKeys)
    cloudmader = wordCloudGenerator()
    cloudmader.generate_wordcloud(fq, mask_path='meatballSpaghetii/integration/resource/goblin.jpg', font_path='meatballSpaghetii/integration/resource/Iansui/Iansui-Regular.ttf')

def summerize(kwGetter, decoder, key):
    text = decoder.makeSentence()
    commentKeys = getKeyword(kwGetter, text, False)
    sentences = [list(jieba.cut(sent)) for sent in text.split("\n")]
    co_occurrence = kwGetter.calculate_co_occurrence(sentences, commentKeys)

    # 篩選包含共現詞對的句子
    list_selected = [''.join(s) for s in sentences if any(c[0][0] in ''.join(s) and c[0][1] in ''.join(s) for c in co_occurrence.items())]
    
    # 過濾掉空評論或只包含冒號(:)的評論
    filtered_sentences = [s for s in list_selected if s and len(s.strip()) > 1 and not s.strip().startswith(':')]
    
    # 只有當有非空評論時才進行情感分析
    if filtered_sentences:
        # 使用 SnowNLP 進行情感分析，並列出每個句子的情感傾向
        sentiment_analyzer = SentimentAnalyzer(custom_model_path='model_training/sentiment.marshal')
        sentence_df = sentiment_analyzer.print_sentence_sentiments(filtered_sentences)
        
        # 可選：將結果保存為 CSV 文件
        # sentence_df.to_csv("sentiment_analysis_result.csv", index=False, encoding='utf-8-sig')
    else:
        print("\n" + "="*20 + " 情感分析結果 " + "="*20)
        print("無有效評論可進行情感分析")
        print("="*55 + "\n")
    
    # 原有的 Gemini API 摘要功能
    summer = summerizer()
    summer.sum(list_selected, key)


try:
    decoder = decodeJson()
    kwGetter = keywordGetter()
    text = input("你想要找甚麼: ")
    key = getKeyword(kwGetter, text, True)

    print("="*50)
    search(decoder, key)
    summerize(kwGetter, decoder, key)

    cloud(kwGetter, decoder)
except Exception as e:
    print ("發生錯誤", e)

