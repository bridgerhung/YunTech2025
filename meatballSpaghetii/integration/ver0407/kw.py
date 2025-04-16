import jieba
import jieba.analyse
from collections import  defaultdict, Counter
import itertools
import re

class keywordGetter:
    keys =[]
    def __init__(self):
        pass
        #替換為自己訓練的模型
    def extract_keywords(self, text, topk=25, dict_path='meatballSpaghetii/integration/ver0407/custom_dict/ecommerce_dict.txt', stop_path='meatballSpaghetii/integration/ver0407/custom_dict/ecommerce_stopwords.txt', modelMode=False):
        if dict_path:
            jieba.set_dictionary(dict_path)
        if stop_path:
            jieba.analyse.set_stop_words(stop_path)
        keys=jieba.analyse.extract_tags(text, topK=topk)
        return keys


    def calculate_co_occurrence(self, sentences, tags, window_size=5):
        
        occurrence = defaultdict(int)
        for sent in sentences:
            for word1, word2 in itertools.combinations(sent, 2):
                if word1 in tags and word2 in tags:
                    occurrence[(word1, word2)] += 1
        return occurrence

    def getFreq(self, text, tags):
        """
        統計 DataFrame 中 col_name 欄位的所有文字中，tags 中每個詞的出現次數。

        :param df: 包含評論的 DataFrame
        :param tags: 想統計出現次數的詞語列表
        :param col_name: 欲分析的欄位名稱，預設為 "評論"
        :return: 一個 dict，key 是詞語，value 是出現次數
        """
        
        word_counts = Counter(jieba.lcut(text))
        freq = {tag: word_counts[tag] for tag in tags}
        return freq

