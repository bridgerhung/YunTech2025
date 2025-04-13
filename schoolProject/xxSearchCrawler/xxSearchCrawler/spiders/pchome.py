import scrapy
from .keywords_filter import deny_keywords
from xxSearchCrawler.items import XxsearchcrawlerItem
import time

class PchomeSpider(scrapy.Spider):

    name = "pchome"
    allowed_domains = ["pchome.com.tw"]
    start_urls = [
        # "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DHAA&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSAA&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSAM&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSAU&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSAB&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAA&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAH&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAB&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAG&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAF&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DCAS&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAI&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSAJ&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAD&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSAZ&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAE&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAC&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DGCD&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DGAG&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DCAR&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DCAX&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSAX&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSAF&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSBE&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DGCA&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAO&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAM&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DRAN&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DGBN&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSBC&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DSAW&page=1&pageCount=100",
        "https://ecshweb.pchome.com.tw/search/v4.3/all/results?cateid=DYCK&page=1&pageCount=100"
    ]





    def productsParse(self, response):
        totalPage = response.json()['TotalPage'] # 產品總數量
        currentPage = int(response.url.split("page=")[1].split("&")[0])  # 現在頁數
        products = response.json()['Prods']
        cateId = response.url.split("cateid=")[1].split("&")[0]

        for product in products:
            if any(deny_keyword in product['Name'] for deny_keyword in deny_keywords):
                continue
            meta = {
                "cateId": cateId,
                "platform": "pchome",
                "title": product['Name'],
                "productId": product['Id'],  # 獲取商品ID 用於向評論API請求
                "price": product['Price'],
                "describe": product['Describe'],
                "spec": "N/A",
                "comments":[]
            }
            yield scrapy.Request(
                f"https://ecapi-cdn.pchome.com.tw/fsapi/reviews/{meta['productId']}/comments?type=all&category=best&attachment=&page=1&limit=3",
                callback=self.commentsParse, meta=meta)
            time.sleep(0.1)
            print("睡0.1秒鐘")
        if (currentPage < totalPage):
            nextPageUrl = response.url.split("page=")[0] + f"&page={currentPage+1}" + "&pageCount=100"
            yield scrapy.Request(nextPageUrl, callback=self.productsParse)

    def commentsParse(self, response):
        if (response.status != 200):
            self.logger.warning(f"Request blocked with {response.status}: {response.url}")
            return

        meta = response.meta
        totalComments = response.json()['Total']  # 總評論數

        if totalComments == 0:  # 沒有評論直接返回
            return
        totalPage = response.json()['TotalPages']  # 總頁數
        currentPage = int(response.url.split("page=")[1].split("&")[0])  # 現在頁數
        comments = response.json()['Rows']



        for comment in comments:  # 顯示評論資訊
            meta['comments'].append({
                "productName": comment['ProdName'],
                "comment": comment['Comments']['User'],
                "star": comment['QualityLikes'],
                "date": comment['ReviewsDate'],
            })


        if (currentPage < totalPage):
            currentPage += 1
            next_page = f"https://ecapi-cdn.pchome.com.tw/fsapi/reviews/{meta['productId']}/comments?type=all&category=best&attachment=&page={currentPage}&limit=3"
            yield scrapy.Request(next_page, callback=self.commentsParse, meta=meta)
        else:
            item = XxsearchcrawlerItem()
            item['cateId'] = meta['cateId']
            item['platform'] = meta['platform']
            item['title'] = meta['title']
            item['productId'] = meta['productId']
            item['price'] = meta['price']
            item['comments'] = meta['comments']
            item['spec'] = meta['spec']
            item['describe'] = meta['describe']
            yield item


    def start_requests(self):
        startTime = time.time()
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.productsParse)
        print("pchome爬蟲用時: "+ str(time.time()-startTime)  + "秒")
