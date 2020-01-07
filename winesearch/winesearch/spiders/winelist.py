# -*- coding: utf-8 -*-
import scrapy


class WinelistSpider(scrapy.Spider):
    name = 'winelist'
    allowed_domains = ['wine-searcher.com']
    start_urls = ['https://www.wine-searcher.com/most-expensive-wines']

    def parse(self, response):
        for url in response.css("tbody > td > a::attr(href)").getall():
            url = response.urljoin(url)
#            yield {"url":url}
        for next_url in response.css("#navigation > ul > li > a::attr(href)").getall():
            next_url = response.urljoin(next_url)
            yield {"other": next_url}
