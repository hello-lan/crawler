# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WinesearchItem(scrapy.Item):
    mongodb_spiders = ["price", "price2"]
    mongodb_collections = ["winesearch_price"]
    # name = scrapy.Field()
    url = scrapy.Field()
    wine = scrapy.Field()
    wine_with_vintage = scrapy.Field()
    vintage = scrapy.Field()
    price = scrapy.Field()
    benchmark = scrapy.Field()
    currency_symbol = scrapy.Field()

