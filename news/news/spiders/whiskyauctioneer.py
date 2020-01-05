# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from news.items import NewsItem

from datetime import datetime


class WhiskyauctioneerSpider(scrapy.Spider):
    name = 'whiskyauctioneer'
    allowed_domains = ['whiskyauctioneer.com']
    start_urls = ['https://www.whiskyauctioneer.com/ajax/news?sort_by=created&sort_order=DESC&items_per_page=All']

    custom_settings = {
        "ITEM_PIPELINES": {
            "news.pipelines.MongoDBPipeline": 301,
        },
        "DOWNLOAD_DELAY": 0.8,
    }

    def parse(self, response):
        for url in response.css(".view-content > .views-row .news-title > a::attr(href)").getall():
            url = response.urljoin(url)
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        item = NewsItem()
        item["url"] = response.url
        item["title"] = response.css("#page-title::text").get("")
        item["author"] = None
        pub_time = response.css("p.date::text").get()
        item["pub_time"] = datetime.strptime(pub_time, "%d.%m.%Y")
        item["content"] = response.css(".contant").get()
        item["crawl_time"] = datetime.now()
        return item
