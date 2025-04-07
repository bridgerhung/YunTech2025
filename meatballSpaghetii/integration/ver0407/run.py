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
    text = decoder.makeSentence()
    commentKeys = getKeyword(kwGetter, text, False)
    sentences = [list(jieba.cut(sent)) for sent in text.split("\n")]
    co_occurrence = kwGetter.calculate_co_occurrence(sentences, commentKeys)

    # Calculate sentence relevance scores based on keyword frequency
    sentence_scores = []
    for i, sent in enumerate(sentences):
        joined_sent = ''.join(sent)
        # Count occurrence of keywords in sentence
        keyword_count = sum(keyword in joined_sent for keyword in commentKeys)
        # Count co-occurrence pairs in sentence
        cooccur_count = sum(1 for c in co_occurrence.items() 
                           if c[0][0] in joined_sent and c[0][1] in joined_sent)
        # Calculate combined score (weight can be adjusted)
        score = keyword_count + (cooccur_count * 2)  # Give more weight to co-occurrence
        sentence_scores.append((i, score, joined_sent))
    
    # Sort sentences by score in descending order and take the top N most relevant
    sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
    top_sentences = [s[2] for s in sorted_sentences[:min(20, len(sorted_sentences))]]
    
    # Filter out very short sentences or sentences without meaningful content
    filtered_sentences = [s for s in top_sentences if len(s) > 10]
    
    # Combine sentences into a well-structured text
    list_selected = "\n".join(filtered_sentences)
    
    summer = summerizer()
    summer.sum(list_selected, key)

decoder = decodeJson()
kwGetter =keywordGetter()
text =input("你想要找甚麼: ")
key=getKeyword(kwGetter, text, True)

print("="*50)
search(decoder, key)
summerize(kwGetter, decoder, key)

cloud(kwGetter, decoder)