# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from datetime import datetime
from news.items import NewsItem


class LivExSpider(scrapy.Spider):
    name = 'liv_ex'
    allowed_domains = ['liv-ex.com']
    start_urls = ['https://www.liv-ex.com/category/liv-ex-blog-chinese-translation/']

    custom_settings = {
        "ITEM_PIPELINES": {
            "news.pipelines.MongoDBPipeline": 301,
        },
        "DOWNLOAD_DELAY": 0.8,
    }

    def parse(self, response):
        for url in response.css("[id|=post] h2.title > a::attr(href)").getall():
            yield Request(url, callback=self.parse_item)
        next_url = response.css("div.next > a::attr(href)").get()
        if next_url:
            yield Request(next_url)

    def parse_item(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['title'] = response.css("h1.entry-title::text").get()
        dt = response.css(".meta-date::text").get()
        item["pub_time"] = datetime.strptime(dt, "%B %d, %Y")
        item["content"] = "".join(response.css(".content-inner > p").getall()[:-3])
        item["crawl_time"] = datetime.now()
        yield item

