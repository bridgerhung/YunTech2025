from decodeJson import decodeJson
from kw import keywordGetter
from summerize import summerizer
import jieba
from cloud import wordCloudGenerator

def search(decoder, keyword):
    
    filtered_df = decoder.search_reviews(keyword)


def getKeyword(kwGetter, inputResult, modelMode):
    
    return kwGetter.extract_keywords(text =inputResult, modelMode =modelMode)

def cloud(kwGetter, decoder):
    text =decoder.makeSentence()
    commentKeys= getKeyword(kwGetter, text, False)
    fq =kwGetter.getFreq(text, commentKeys)
    #print(fq)
    cloudmader =wordCloudGenerator()
    cloudmader.generate_wordcloud(fq, mask_path='meatballSpaghetii/integration/resource/goblin.jpg', font_path ='meatballSpaghetii/integration/resource/Iansui/Iansui-Regular.ttf')

def summerize(kwGetter, decoder, key):
    text =decoder.makeSentence()
    commentKeys= getKeyword(kwGetter, text, False)
    sentences = [list(jieba.cut(sent)) for sent in text.split("\n")]
    co_occurrence = kwGetter.calculate_co_occurrence(sentences, commentKeys)

    # 輸出共現分析結果
    #print('\n================共現分析=================')
    #print(sorted(co_occurrence.items(), key=lambda x: x[1], reverse=True)[:10])
    list_selected = [''.join(s) for s in sentences if any(c[0][0] in ''.join(s) and c[0][1] in ''.join(s) for c in co_occurrence.items())]
    for i in list_selected:
        #print(i, end ="\n\n")
        pass
    summer =summerizer()
    summer.sum(list_selected, key)
    



    
decoder = decodeJson()
kwGetter =keywordGetter()
text =input("你想要找甚麼: ")
key=getKeyword(kwGetter, text, True)



print("="*50)
search(decoder, key)
summerize(kwGetter, decoder, key)

cloud(kwGetter, decoder)