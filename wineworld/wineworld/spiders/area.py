# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

import re

from wineworld.items import AreaRegionItem, AreaCountryItem


class AreaSpider(scrapy.Spider):
    name = 'area'
    allowed_domains = ['wine-world.com']
    start_urls = ['https://m.wine-world.com/area']


    def parse(self, response):
        for url in response.css("ul.wine-r-list > li > a::attr(href)").getall():
            yield Request(url, callback=self.parse_country)

    def parse_country(self, response):
        item = AreaCountryItem()
        item["url"] = response.url
        item["country_en"] = response.css(".reg-tit::text").get()
        item["country_cn"] = response.css(".tit-en::text").get()
        item["intro"] = "".join(response.css("article p *::text").re("\S.*\S"))
        item["regions"] = response.css("ul.reglist > li > a::text").re("\S.*\S")
        yield item

        for url in response.css("ul.reglist > li > a::attr(href)").getall():
            yield Request(url, callback=self.parse_region)

    def parse_region(self, response):
        item = AreaRegionItem()
        item["url"] = response.url
        item["country"] = re.findall("/area/([^/]+)/", response.url)[0]
        item["region_name_cn"] = response.css(".mbox > .reg-tit::text").get()
        item["region_name_en"] = response.css("span.tit-en::text").get()
        info = {}
        for tmp_sel in response.css(".grape-attr > dl"):
            key = tmp_sel.css("dt::text").get("").strip()
            value = tmp_sel.css("dd::text").get("").strip()
            info[key] = value
        item["region_info"] = info
        item["intro"] = "".join([s for s in response.css("article p::text").re("\S.*\S") if len(s.strip()) > 0])
        yield item

        for url in response.css("ul.reglist > li > a::attr(href)").getall():
            yield Request(url, callback=self.parse_region)

