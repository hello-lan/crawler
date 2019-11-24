# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from wineworld.items import WineryItem, WineryWineItem

import json


class WinerySpider(scrapy.Spider):
    name = 'winery'
    allowed_domains = ['wine-world.com']
    start_urls = []
    entry_url = "https://m.wine-world.com/winery/ajax/AreaSearchAjax"

    winery_wines_url = "https://m.wine-world.com/winery/ajax/wine"

    def start_requests(self):
        yield scrapy.FormRequest(
                self.entry_url,
                formdata={"id": "all", "page": "1"},
                callback=self.parse,
                meta={"page": 1}
                )

    def parse(self, response):
        jdata = json.loads(response.text)
        for row in jdata["rows"]:
            url = row["url"]
            yield Request(url, callback=self.parse_winery_item)
        page_count = jdata["pageCount"]
        page = response.meta["page"]
        if page < page_count:
            page += 1
            yield scrapy.FormRequest(
                    self.entry_url,
                    formdata={"id": "all", "page": str(page)},
                    callback=self.parse,
                    meta={"page": page}
                    )

    def parse_winery_item(self, response):
        item = WineryItem()
        item["url"] = response.url
        item["intro"] = "".join(response.css("#content > .showMoreNChildren p::text").re("\S.*\S"))
        item["winery_en"] = response.css(".winery-tit::text").get()
        item["winery_cn"] = response.css("span.win-en::text").get()
        item["winery_img"] = response.css(".wineryimg > img::attr(src)").get()
        keys = response.css(".grape-attr:nth-child(2) > dl > dt::text").getall()
        values = response.css(".grape-attr:nth-child(2) > dl > dd::text").getall()
        item["base_info"] = dict(zip(keys, values))
        keys2 = response.css(".grape-attr:nth-child(4) > dl > dt::text").getall()
        values2 = response.css(".grape-attr:nth-child(4) > dl > dd::text").getall()
        item["extra_info"] = dict(zip(keys2, values2))
        item["winery_id"] = winery_id = response.url.split("/")[-1]
        yield item

        yield scrapy.FormRequest(
                self.winery_wines_url,
                formdata={"id": winery_id, "page": "1"},
                callback=self.parse_wine_item,
                meta={"page":1, "winery_id":winery_id}
                )

    def parse_wine_item(self, response):
        winery_id = response.meta["winery_id"]
        jdata = json.loads(response.text)
        for row in jdata["rows"]:
            item = WineryWineItem()
            item["winery_id"] = winery_id
            item["wine_id"] = row["id"]  
            yield item

        page_count = jdata["pageCount"]
        page = response.meta["page"]
        if page < page_count:
            page += 1
            yield scrapy.FormRequest(
                    self.winery_wines_url,
                    formdata={"id": winery_id, "page": str(page)},
                    callback=self.parse_wine_item,
                    meta={"page":page, "winery_id":winery_id}
                    )
