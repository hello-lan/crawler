# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

import os
from whiskyauctioneer.items import Item

cur_dir = os.path.dirname(__file__)


class PastAuctionsSpider(scrapy.Spider):
    name = 'past_auctions'
    allowed_domains = ['whiskyauctioneer.com']
    start_urls = ['https://www.whiskyauctioneer.com/november-2019-auction?s=5e118933ef361']

    custom_settings = {
        "ITEM_PIPELINES": {
            "whiskyauctioneer.pipelines.MongoDBPipeline":301,
        },
    }


    def __init__(self, begin=0, end=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.begin = int(begin)
        self.end = int(end)

    def start_requests(self):
        print("read urls...")
        fpath = os.path.join(cur_dir, "urls.csv")
        with open(fpath) as f:
            urls = [url.strip() for url in f]

        start, end = self.begin, self.end
        for url in urls[start:end]:
            print(url)
            yield Request(url)

    def parse(self, response):
        title = response.css("#page-title::text").get()
        for sel in response.css("#homepage-product-listing div[id|=block-views] > .views-row"):
            url = sel.css(".views-field-title > span.field-content > a::attr(href)").get()
            url = response.urljoin(url)
            end_date = sel.css(".enddatein > span::text").get()
            yield Request(url, meta={"end_date":end_date, "page_title":title}, callback=self.parse_item)

        for next_url in response.css(".item-list > ul > li > a::attr(href)").getall():
            next_url = response.urljoin(next_url)
            yield Request(next_url)

    def parse_item(self, response):
        item = Item()
        item["category"] = response.meta["page_title"]
        item["end_date"] = response.meta["end_date"]
        item["url"] = response.url
        item["lot"] = response.css("lot").re_first("\d+")
        item["name"] = response.css(".left-heading > h1::text").get()
        item["images"] = response.css(".views-field-uc-product-image img::attr(src)").getall()
        item["price"] = response.css(".bid-info > .winning > .uc-price::text").get()
        item["base_info"] = response.css("span.field-content > whiskyproduct").get()
        item["intro"] = response.css(".rightvbn .field-content").get()
        item["recommendations"] = response.css("#block-current-auction-recommendations span.lotnumber::text").re("\d+")
        return item
