# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request

from winesearch.items import WinesearchItem

from http.cookies import SimpleCookie


def process_cookie_str(s):
    cookie = SimpleCookie(s)
    cookie_dict = {k:v.value for k, v in cookie.items()}
    return cookie_dict

    
s = "cookie_enabled=true; cookie_enabled=true; cookie_enabled=true; visit=4GMVC84NDCP003G%7C20191209150107%7C%2F%7Chttps%253A%252F%252Fcn.bing.com%252F%7Cend+; _csrf=MBTPTLnd3MtDFH0Ru0oyP3DNxbRLFwCj; _pxvid=0d980c1e-1a95-11ea-8159-0242ac12000d; __gads=ID=a1f4c6f6206a508f:T=1575904270:S=ALNI_Ma0PEVbiX-5C1auo8iyLiFpm910MQ; OX_plg=pm; __pxvid=31d2dbb2-1b52-11ea-9214-0242ac110003; COOKIE_ID=NBDVCCXTD6B00DH; geoinfo=31.0449|121.4012|Shanghai|China|CN|101.86.243.81|1796236|IP|Shanghai%2C+China; x=1; fflag=flag_store_manager%3A0%2Cend; ID=RJDWCR49DNF00MZ; IDPWD=I70311573; _gid=GA1.2.1418561016.1577020342; search=start%7Cdom%2Bleroy%2Bmusigny%2Bgrand%2Bcru%2Ble%2Bchambolle%2Bcote%2Bde%2Bnuit%2Bburgundy%2Bfrance%7C1%7Cany%7CCNY%7C%7C%7C%7C%7C%7C%7C%7C%7Ce%7Cend; _gat_UA-216914-1=1; ws_prof=145944%7C71377282%7C0; _ga=GA1.1.1423871730.1575903807; _ga_M0W3BEYMXL=GS1.1.1577020320.17.1.1577022375.0; _px3=7f6ad22ae3a68739665e10d313ba00013201b28e01a83e9f22f4714f6b5d1665:qdlGpcy2yiqkxXZDd/Ei+5u5BrfqjBRPYm/N4SH7CbWjn5HaTRZM1gpXVAiVtsYhXzalsdJGJbN9Hd0T1OE1yw==:1000:X0kVtWR6NFp1mxUV/szGaK0mNmGmVzoiHa3jxHS/4gQeTOHJJcY+5l9XWOicXlk/Ik3ndldszFPinxGaxXLXggkmWbibFNIRfjeCuI0fzQQqCIPk7M3jOQi9U6vD4Wy29uiP8AjKN2h5p8icAwb0vO3fMZIkcoJ5DsD9nu6kMGE=; _pxde=3949cf29f549a5c4f6914edbdef947b2b6e16e7a17edc338657a0ebd259955a6:eyJ0aW1lc3RhbXAiOjE1NzcwMjIzOTgzOTcsImZfa2IiOjAsImlwY19pZCI6W119"
cookies = process_cookie_str(s)

headers = {
 "Referer": "https://www.wine-searcher.com/sign-in?pro_redirect_url_F=/find/dom+leroy+musigny+grand+cru+le+chambolle+cote+de+nuit+burgundy+france/-/any",
 "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36",
 "Accept-Language": "zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7",
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
 "Accept-Encoding": "gzip, deflate, br",
 "Cookie": s,
 "upgrade-insecure-requests": 1,
 "sec-fetch-user": "?1",
 "sec-fetch-site": "same-origin",
 "sec-fetch-mode": "navigate",
 "cache-control": "max-age=0",
}


class Price2Spider(scrapy.Spider):
    name = 'price2'
    allowed_domains = ['wine-searcher.com']
    start_urls = ['https://www.wine-searcher.com/find/montrose+st+estephe+medoc+bordeaux+france/1997/china?Xbottle_size=all&Xprice_set=CUR&Xshow_favourite=N#t3']
    # start_urls = ['https://www.wine-searcher.com/find/dom+leroy+musigny+grand+cru+le+chambolle+cote+de+nuit+burgundy+france/-/any']
    login_url = "https://www.wine-searcher.com/sign-in?pro_redirect_url_F=/"

    custom_settings = {
        "DOWNLOAD_DELAY": 20,
        "DEFAULT_REQUEST_HEADERS":headers,
        "ITEM_PIPELINES": {
            "winesearch.pipelines.MongoDBPipeline": 301,
        },
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        s = response.css("#hst_price_div_detail_page::attr(data-chart-data)").get()
        with open("test.html", 'w') as f:
            f.write(response.text)
        try:
            data = json.loads(s)
        except:
            pass
        else:
            chart_data = data["chartData"]
            item = WinesearchItem()
            item["url"] = response.url
            item["wine"] = response.css("#imgThumbDiv::attr(data-labels-alt)").get()
            item["wine_with_vintage"] = "".join([s.strip() for s in response.css("h1 span::text").getall()])
            item["vintage"] = response.css("#Xvintage::attr(value)").get()
            item["price"] = chart_data["main"]
            item["benchmark"] = chart_data["bm"]
            item["currency_symbol"] = chart_data["currencySymbol"]
            yield item

        for _vintage_url in response.css("ul.vtglist > li > a::attr(href)").getall():
            vintage_url = "https://www.wine-searcher.com" + _vintage_url
            yield Request(vintage_url)


