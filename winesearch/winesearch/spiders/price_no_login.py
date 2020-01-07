# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
from winesearch.items import WinesearchItem



class PriceNoLoginSpider(scrapy.Spider):
    name = 'price_no_login'
    allowed_domains = ['wine-searcher.com']
    start_urls = ['https://www.wine-searcher.com/find/dom+george+christoph+roumier+musigny+grand+cru+le+chambolle+cote+de+nuit+burgundy+france/-/china#t31']

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
            item["wine_with_vintage"] = "".join([s.strip() for s in response.css("h1 span::text").getall()])
            item["vintage"] = response.css("#Xvintage::attr(value)").get()
            item["price"] = chart_data["main"]
            item["benchmark"] = chart_data["bm"]
            item["currency_symbol"] = chart_data["currencySymbol"]
            yield item

        for _vintage_url in response.css("ul.vtglist > li > a::attr(href)").getall():
            vintage_url = "https://www.wine-searcher.com" + _vintage_url
            yield Request(vintage_url)


