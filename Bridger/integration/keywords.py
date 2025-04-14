import jieba
import jieba.analyse
from collections import  defaultdict, Counter
import itertools
import re

class keywords:
    def extract_keywords(self, text, topk=25, dict_path='meatballSpaghetii/integration/resource/dict (1).txt', stop_path='meatballSpaghetii/integration/resource/stopwords (1).txt', modelMode=False):
        if dict_path:
            jieba.set_dictionary(dict_path)
        if stop_path:
            jieba.analyse.set_stop_words(stop_path)
        if modelMode:
            parts = re.findall(r'[a-zA-Z]+|\d+', text)
            if len(parts) >= 2:
                text += " " + " ".join(parts)  # 把英數加進原始 text
        keys=jieba.analyse.extract_tags(text, topK=topk)
        return keys

    def occurrence(self, sentenceList, keywords, ):
        analysis =defaultdict(int)
        for s in sentenceList:
            for word1, word2 in itertools.combinations(s, 2):
                if word1 in keywords and word2 in keywords:
                    analysis[(word1, word2)] += 1
        return analysis
    
    def getFreq(self, text, keywords):
        """
        統計 DataFrame 中 col_name 欄位的所有文字中，tags 中每個詞的出現次數。

        :param df: 包含評論的 DataFrame
        :param tags: 想統計出現次數的詞語列表
        :param col_name: 欲分析的欄位名稱，預設為 "評論"
        :return: 一個 dict，key 是詞語，value 是出現次數
        """
        
        word_counts = Counter(jieba.lcut(text))
        freq = {key: word_counts[key] for key in keywords}
        return freq


keywordGetter =keywords()
print(keywordGetter.extract_keywords("Iphone16", modelMode =True))