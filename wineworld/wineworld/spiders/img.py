# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from wineworld.items import ImageItem


class ImgSpider(scrapy.Spider):
    name = 'img'
    allowed_domains = ['wine-world.com']
    start_urls = ['http://wine-world.com/']
    
    custom_settings = {
        "ITEM_PIPELINES": {
            "wineworld.pipelines.MyImagesPipeline": 300,
            "wineworld.pipelines.MongoDBPipeline": 301,
        },
        "IMAGES_STORE": "images",
        "IMAGES_URLS_FIELD": "url"
    }

    def __init__(self, fpath=None, *args, **kwargs):
        super(ImgSpider, self).__init__(*args, **kwargs)
        self.fpath = fpath

    def parse(self, response):
        # url = "https://article-picture.wine-world.com/5ea53829-d4bc-4f48-8945-62081be818bd.jpg"
        with open(self.fpath) as f:
            for url in f.readlines():
                item = ImageItem()
                item["url"] = url.strip()
                yield item
