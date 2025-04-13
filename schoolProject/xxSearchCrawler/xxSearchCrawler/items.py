# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XxsearchcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 建立商品評論的資料欄位
    productName = scrapy.Field() # 產品點進去後頁面標題的名稱 (有評論那)
    comments = scrapy.Field()
    star = scrapy.Field()
    date = scrapy.Field()

    # 建立商品資訊的資料欄位
    title = scrapy.Field() # 產品未點進去頁面時的名稱
    productId = scrapy.Field()
    price = scrapy.Field()
    platform = scrapy.Field()
    cateId = scrapy.Field()
    spec = scrapy.Field()
    describe = scrapy.Field()