# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    mongodb_spiders = ["decanterchina", "liv_ex"]
    mongodb_collections = ["news"]

    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    pub_time = scrapy.Field()
    content = scrapy.Field()
    # img_urls = scrapy.Field()
    crawl_time = scrapy.Field()
