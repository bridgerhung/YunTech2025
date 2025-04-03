# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from distutils.command.install_egg_info import safe_name

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os, json




class XxsearchcrawlerPipeline:
    def __init__(self):
        self.files = {}

    # 爬蟲開始時，建立資料夾 (會自動執行)
    def open_spider(self, spider):
        self.outputDir = "output_comments"
        os.makedirs(self.outputDir, exist_ok=True)

    # 爬蟲執行時，將資料存入self.files[對應的path] (使用yeild後 會將資料傳至這裡 進行處理)
    def process_item(self, item, spider):

        cate = item['cateId']
        safeName = safe_name(cate)
        filePath = os.path.join(self.outputDir, f'output_{safeName}.json')

        if filePath not in self.files:
            self.files[filePath] = []
        self.files[filePath].append(       {
            "分類": item["cateId"],
            "產品頭銜": item['title'],
            "平台來源": item['platform'],
            "產品規格": item['spec'],
            "產品介紹": item['describe'],
            "產品價錢": item["price"],
            "評論": []
                }
            )
        for comment in item['comments']:

            comments = {
                "產品名稱": comment['productName'],
                "評論":comment['comment'],
                "星數":comment['star'],
                "日期":comment['date']
            }

            self.files[filePath][len(self.files[filePath])-1]["評論"].append(comments)
        # 這裡要return item，因為這個item要傳給下一個pipeline (而且不管怎樣都要return item, 就算你沒有下一個pipeline)
        return item

    # 爬蟲結束時，將所有資料寫入檔案 (會自動執行)
    def close_spider(self, spider):
        for filePath, comments in self.files.items():
            with open(filePath, 'w', encoding='utf-8') as f:
                json.dump(comments, f, ensure_ascii=False, indent=4)