# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from wineworld.items import GrapeItem


class GrapeSpider(scrapy.Spider):
    name = 'grape'
    allowed_domains = ['wine-world.com']
    start_urls = ['https://m.wine-world.com/grape']

    def parse(self, response):
        for url in response.css("#isEn > li > a[id]::attr(href)").getall():
            url = response.urljoin(url)
            yield Request(url,
                          callback=self.parse_letter_category,
                          )

    def parse_letter_category(self, response):
        for url in response.css("#showResult .vinbox > a::attr(href)").getall():
            url = response.urljoin(url)
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        item = GrapeItem()
        item["url"] = response.url
        item["name_en"] = response.css(".tit-en::text").get("").strip()
        item["name_cn"] = response.css(".reg-tit::text").get("").strip()
        keys = response.css("div.grape-attr > dl > dt::text").getall()
        values = response.css("div.grape-attr > dl > dd::text").getall()
        item["attr"] = dict(zip(keys, values))
        item["img"] = response.css("article > p:nth_child(1) > img::attr(src)").get()
        item["intro"] = response.css("div.grape-attr, article.aritcle-info").getall()
        yield item

