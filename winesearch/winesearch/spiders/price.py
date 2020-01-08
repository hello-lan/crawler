# -*- coding: utf-8 -*-
import scrapy
import json
import csv
from scrapy.http import Request
from winesearch import settings
from winesearch.items import WinesearchItem



class PriceSpider(scrapy.Spider):
    name = 'price'
    allowed_domains = ['wine-searcher.com']
    start_urls = ['https://www.wine-searcher.com/find/montrose+st+estephe+medoc+bordeaux+france/1997/china?Xbottle_size=all&Xprice_set=CUR&Xshow_favourite=N#t3']
    login_url = "https://www.wine-searcher.com/sign-in?pro_redirect_url_F=/"

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "DOWNLOADER_MIDDLEWARES": {
#            "winesearch.middlewares.UserAgentMiddleware": 300,
            "winesearch.middlewares.ProxyMiddleware": 100,
            "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": None,
        },
        "ITEM_PIPELINES": {
            "winesearch.pipelines.MongoDBPipeline": 301,
        },
    }

    def __init__(self, fpath=None, *args, **kwargs):
        super(PriceSpider, self).__init__(*args, **kwargs)
        self.fpath = fpath

    def start_requests(self):
        print(settings.ACCOUNT)
        yield Request(self.login_url, callback=self.login, meta={"use_proxy":True})

    def login(self, response):
        data = {"LoginModel[username]":settings.ACCOUNT,
                "LoginModel[password]": settings.PASSWORD,
                "LoginModel[rememberMe]": "1",
                }
        yield scrapy.FormRequest.from_response(response, 
                                               formdata=data,
                                               callback=self.after_login,
                                               dont_filter=True,
                                               meta={"use_proxy":True}
                                              )

    def after_login(self, response):
        with open(self.fpath) as f:
            csv_reader = csv.reader(f, delimiter=",")
            for row in csv_reader:
                url = row[0]
                yield Request(url)

    def parse(self, response):
        s = response.css("#hst_price_div_detail_page::attr(data-chart-data)").get()
        try:
            data = json.loads(s)
        except:
            pass
        else:
            chart_data = data["chartData"]
            item = WinesearchItem()
            item["url"] = response.url
            item["wine"] = response.css("#imgThumbDiv::attr(data-labels-alt)").get()
            item["wine_with_vintage"] = response.css("#top_header > span[itemprop=name]::text").get().strip()
            item["vintage"] = response.css("td.text-centered > span.current-vint::text").get().strip()
            item["price"] = chart_data["main"]
            item["benchmark"] = chart_data["bm"]
            item["currency_symbol"] = chart_data["currencySymbol"]
            yield item

            for _vintage_url in response.css("#scroll_table tr > td.text-centered > a::attr(href)").getall():
                vintage_url = response.urljoin(_vintage_url)
                yield Request(vintage_url)

