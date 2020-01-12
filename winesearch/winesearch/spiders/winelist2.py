# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from winesearch import settings


class Winelist2Spider(CrawlSpider):
    name = 'winelist2'
    allowed_domains = ['wine-searcher.com']
    start_urls = ['https://www.wine-searcher.com/most-expensive-wines']
    login_url = "https://www.wine-searcher.com/sign-in?pro_redirect_url_F=/"

    custom_settings = {
        "DOWNLOAD_DELAY": 50,
        "DOWNLOADER_MIDDLEWARES": {
            "winesearch.middlewares.SleepMiddleware": 100,
        },
    }

    rules = (
        Rule(LinkExtractor(allow=r'/regions-', restrict_css=("#navigation > ul", "#winesortlist > .s-tab-row")), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        data = {"LoginModel[username]":settings.ACCOUNT,
                "LoginModel[password]": settings.PASSWORD,
                "LoginModel[rememberMe]": "1",
                }
        yield scrapy.FormRequest.from_response(response, 
                                               formdata=data,
                                               callback=self.after_login,
                                               dont_filter=True,
                                              )

    def after_login(self, response):
        for url in self.start_urls:
            yield Request(url)

    def parse_item(self, response):
        for url in response.css("table.nltbl td>a::attr(href)").getall():
            item = {"url": response.urljoin(url)}
            yield item
