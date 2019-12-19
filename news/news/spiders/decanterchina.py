# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

import re
from itertools import chain
from datetime import datetime

from news.items import NewsItem


class DecanterchinaSpider(scrapy.Spider):
    name = 'decanterchina'
    allowed_domains = ['decanterchina.com']
    start_urls = ['https://www.decanterchina.com/zh/%E8%A1%8C%E4%B8%9A%E6%96%B0%E9%97%BB/']

    custom_settings = {
        "ITEM_PIPELINES": {
            "news.pipelines.MongoDBPipeline": 301,
        },
        "DOWNLOAD_DELAY": 0.8,
    }

    def parse(self, response):
        urls_1 = response.css(".featured h1 > a::attr(href)").getall()
        urls_2 = response.css(".featured-sub-item h2 > a::attr(href)").getall()
        urls_3 = response.css(".featured-list-item h3.medium > a::attr(href)").getall()
        for url in chain(urls_1, urls_2, urls_3):
            url = response.urljoin(url)
            yield Request(url, callback=self.parse_item)

        for next_url in response.css(".pagination > ul > li > a::attr(href)").getall():
            next_url = response.urljoin(next_url)
            yield Request(next_url)

    def parse_item(self, response):
        item = NewsItem()
        item["url"] = response.url
        item["title"] = response.css("header > h1::text").get('').strip()
        item["author"] = response.css(".author > [rel=author]::attr(title)").get()
        ts = response.css("time::attr(datetime)").get()
        item["pub_time"] = datetime.fromtimestamp(int(ts))

        def rpl(m):
            url_ = m.group("url")
            txt = m.group()
            url = response.urljoin(url_)
            rpl_txt = txt.replace(url_, url)
            return rpl_txt

        txt =  ''.join(response.css("div.article-content > :not(div)").getall())
        item["content"] = re.sub("src=\"(?P<url>.*?\.jpg)\"", rpl, txt)
        item["crawl_time"] = datetime.now()
        return item
