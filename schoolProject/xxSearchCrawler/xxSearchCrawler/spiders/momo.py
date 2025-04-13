import json
import scrapy
from scrapy.http import JsonRequest
from scrapy import FormRequest
from xxSearchCrawler.items import XxsearchcrawlerItem

class MomoSpider(scrapy.Spider):
    name = "momo"
    allowed_domains = ["momoshop.com.tw"]
    productsUrl = "https://www.momoshop.com.tw/ajax/ajaxTool.jsp?n=2022&t=1744385549330"
    commentsUrl = "https://eccapi.momoshop.com.tw/user/getGoodsCommentList"
    start_urls = []
    '''
    todo: 用seleium抓新cookie值
    '''
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://www.momoshop.com.tw/",
        "X-Requested-With": "XMLHttpRequest",
        'Connection': 'Keep-Alive',
        'origin': 'https://www.momoshop.com.tw',
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        'cookie': "_mwa_uniCampaignInfo=1741697324031987740.1741697324031; _gcl_au=1.1.196196339.1741697326; _edvid=2bba07b0-fe77-11ef-967e-fd94b618ddd1; _atrk_siteuid=EYThJNYKHeKGyyuf; ARK_ID=JS062d95478008b81348cbef83dbc63422062d; _gcl_gs=2.1.k1$i1742437494$u221022084; _gcl_aw=GCL.1742437498.Cj0KCQjw1um-BhDtARIsABjU5x5Brx726JXN2-zrNz_O63NPtFoseV8GA5ZNRSBb7-EZn0EzQhzhabUaAo-6EALw_wcB; appier_utmz=%7B%22csr%22%3A%22google%22%2C%22timestamp%22%3A1743940073%2C%22lcsr%22%3A%22google%22%7D; _tt_enable_cookie=1; _ttp=01JR5TQZCW1MWETK6SWREXC1DY_.tt.2; searchKeyWordsRecord=%5B%22%E5%AF%B5%E7%89%A9%E8%B7%91%E6%AD%A5%E6%A9%9F%22%5D; _gid=GA1.3.1605109611.1744473256; _ga=GA1.1.1463297700.1741697324; TN=undefined; CN=undefined; CM=undefined; bid=4d725da09d45c8a4a99fab90003e64ea; isBI=1; wshop_nontw=wshop_web_c_4; appier_random_unique_id_Conversion_36db=iW6kvvdAuWO2q1W4PJs4h1; ttcsid=1744474973804.2.1744474973804; ttcsid_COTIQNJC77UF1T0I5440=1744474973803.2.1744474974015; GoodsBrowsingHistory=13075340_1737750213/12901802_1736571953/13518430_1743483666/12129356_1735362165; wshop=wshop_web_c_33; _eds=1744526173; _atrk_ssid=qA3LOygDikZJOqsjqNDA76; appier_page_isView_ERlDyPL9yO7gfOb=6170e190cd223f49d1454ed294a313d62a10ea544e010e42db0bec98f3cd132c; appier_pv_counterc7279b5af7b77d1=0; appier_page_isView_c7279b5af7b77d1=6170e190cd223f49d1454ed294a313d62a10ea544e010e42db0bec98f3cd132c; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%2C%22expiryDate%22%3A%222026-04-13T06%3A36%3A14.211Z%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%224zYMDZq48d0PJemeft59%22%2C%22expiryDate%22%3A%222026-04-13T06%3A36%3A14.213Z%22%7D; _mwa_uniVisitorInfo=1741697324031929459.1741697324031.19.1744526174542; cto_bundle=ZR4B-V9vSVAyTyUyRkRNSE9UaVBEbSUyQndQZjFPQW1oY3d1dWdKeXQ4UVBHbm9vYlU0Z1RjNWJxYVV2cFI1TVVvazh4cmdYMHBjZDlacUFqNGJvM1B6bEY4ZDFNc2xMYnVtUk1FQ0Y1czY1SDhERUdnakcyZ2pqQ0FUMVVuU2E2cHpHcEc1WlEzWWxUZ1l0UDY2Nm5nZVlOenBzblUwUHlZTHZ3MWUlMkZQdmVsZnc3U0VJYThRdWtVR2NwSGclMkYwa3BpZTBhVjUlMkZLVzVUZ2RWQiUyRktvUnp5SlJ6c05sc3FBJTNEJTNE; _vid=1c1b48aee6eb22d7fbe15c8739cb64f24dc288bcac8f66015b9e05e2927d7958ea3ecc11a02ad5f2f51ce849de5bad784dd4fac50273953c654f9f2be1e7abb990c0a31dda6d9becc3a92561307771ed1c2729ebc6254c2895d60abce64265d7; _mwa_uniSessionInfo=1744526174542483906.1744526174542.2.1744526176542; _ga_BKEC67VMMG=GS1.1.1744526172.25.1.1744526731.60.0.0; appier_pv_counterERlDyPL9yO7gfOb=1; _atrk_sessidx=7; JSESSIONID=E7D98B9773530BF713D39DB112893574-m1.c1-shop33"
    }
    cateCodeList = [
         "4201500000",
        "4201700000", "4201600000",
        "4201200000", "4201400000", "4201300000",
        "4202500000", "4202700000", "4202600000", "4202800000", "4202100000", "4202200000", "4202300000",
        "4201800000", "4201900000", "4202000000", "4202400000", "5300300000",
        "1912300000", "1912900000", "1905200000", "1908900000", "1901100000", "1902200000", "1904900000",
        "1911100000",
        "1905500000", "1901200000", "1908600000", "1905700000",
        "1911500000", "1911600000", "1911700000", "1911800000", "1912000000", "1912100000", "1911900000",
        "4304300000", "4300100000", "4300200000", "4300300000", "4300400000", "4301700000", "4300500000",
        "4300700000",
        "4300800000", "4300900000", "4301000000", "4301100000", "5300100000", "4304400000",
        "4301800000", "4302200000", "4302000000", "4302500000", "4302300000", "4302600000",
        "4303700000", "4303800000", "4303900000", "4304000000", "4304100000", "4304200000"
    ]
    # 必須重新定義start_request , 因為要發送post請求
    def start_requests(self):

        for code in self.cateCodeList:

            data = {"flag": 2022,
                    "data": {"params": {
                        "cateCode": f"{code}", "cateLevel": "1", "cp": "N", "NAM": "N", "normal": "N"
                        , "first": "N", "freeze": "N", "superstore": "N", "tvshop": "N", "china": "N", "tomorrow": "N",
                        "stockYN": "N", "prefere": "N", "threeHours": "N", "video": "N", "cycle": "N", "cod": "N",
                        "superstorePay": "N", "curPage": "1", "priceS": "0", "priceE": "9999999", "brandName": [],
                        "searchType": "6"}}}
            dataJson = json.dumps(data)
            body = {
                'data': dataJson
            }
            yield FormRequest(url=self.productsUrl,method='POST',formdata=body,
                              headers=self.headers,callback=self.productParse, meta={'formData': data, 'cateId': code})

    def productParse(self, response):
        try:
            if response.status == 200:

                goodsCodeList = []
                res = response.json()

                maxPage = res["rtnData"]["searchResult"]['rtnSearchData']["maxPage"]
                curPage = res['rtnData']['searchResult']['rtnSearchData']['currentPage']
                productList = res['rtnData']['searchResult']['rtnSearchData']['goodsInfoList']

                data = response.meta['formData']
                data['data']['params']['curPage'] = str(int(curPage) + 1)
                dataJson = json.dumps(data)
                formData = {
                    'data': dataJson,
                }

                '''
                todo1: 處理資料環節
                方法: 請迴圈跑抓到的產品資料 取裡面的商品代碼 並存至容器中
                goodsCodeList:儲存商品代碼的容器
                productList: 所有的商品資料
                
                todo2: 將商品資料包成meta傳給評論處理
                # 商品資訊的資料欄位
                title -> 爬蟲資料.goodsName
                productId -> 爬蟲資料.goodsCode
                price -> 爬蟲資料.goodsPrice
                platform -> momo
                cateId -> meta['cateId']
                spec -> null
                describe -> 爬蟲資料.goodsSubName
                '''




                for product in productList:
                    title = product['goodsName']
                    goodsCode = product['goodsCode']
                    price = product['goodsPrice']
                    platform = "momo"
                    cateId = response.meta['cateId']
                    spec = "N/A"
                    describe = product['goodsSubName']
                    print(f"{'='*50}/n商品代碼:{goodsCode}/n{'='*50}")

                    body = {
                        'host': 'momoshop',
                        'curPage': "1",
                        'custNo': '',
                        'filterType': 'hasComment',
                        'goodsCode': f'{goodsCode}',
                        'multiFilterType': ['hasComment']
                    }

                    yield JsonRequest(url=self.commentsUrl, data = body ,
                                      callback=self.commentParse,
                                      meta={
                                            'title': title,
                                            'goodsCode': goodsCode,
                                            'price': price,
                                            'platform': platform,
                                            'cateId': cateId,
                                            'spec': spec,
                                            'describe': describe,
                                            "comments": [],
                                            "curPage": 1
                                            })
                if curPage < maxPage:
                    yield FormRequest(url=self.productsUrl, method='POST', formdata=formData,
                                      headers=self.headers, callback=self.productParse,
                                      meta={'formData': data, 'cateId': response.meta['cateId']})



            else:
                print(f"status code:{response.status}")

        except Exception as e:
            print("發生錯誤: ", e)


    def commentParse(self, response):
        if (response.status == 200):

            maxPage = response.json()['maxPage']
            nextPage = response.meta['curPage'] +1
            if (maxPage > 0):
                comments = response.json()['goodsCommentList']
                for comment in comments:
                    response.meta['comments'].append({
                        'productName': response.meta['title'],
                        'comment': comment['comment'],
                        'star': comment['score'],
                        'date': comment['date'],
                    })

            if nextPage <= maxPage:
                body = {
                    'host':'web',
                    'curPage':nextPage,
                    'custNo':'',
                    'filterType':'hasComment',
                    'goodsCode':f'{response.meta["goodsCode"]}',
                    'multiFilterType':['hasComment']
                }
                yield JsonRequest(url=self.commentsUrl, data=body,
                                  callback=self.commentParse,
                                  meta=response.meta)
            else:
                '''
                todo: 將資料儲存至設定好的item欄位 傳至pipeline做處理
                # 商品評論的資料欄位
                productName -> response.meta['title']
                comments -> comment['comment']
                star -> comment['score']
                date -> comment.['date']
                
                title -> 爬蟲資料.goodsName
                productId -> 爬蟲資料.goodsCode
                price -> 爬蟲資料.goodsPrice
                platform -> momo
                cateId -> meta['cateId']
                spec -> null
                describe -> 爬蟲資料.goodsSubName
                '''
                print(response.meta)
                item = XxsearchcrawlerItem()
                item['title'] = response.meta['title']
                item['productId'] = response.meta['goodsCode']
                item['price'] = response.meta['price']
                item['platform'] = response.meta['platform']
                item['cateId'] = response.meta['cateId']
                item['spec'] = response.meta['spec']
                item['describe'] = response.meta['describe']
                item['comments'] = response.meta['comments']

                yield item
        else:
            pass
