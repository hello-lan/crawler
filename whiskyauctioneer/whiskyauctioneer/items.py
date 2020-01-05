# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WhiskyauctioneerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Item(scrapy.Item):
    mongodb_spiders = ["past_auctions"]
    mongodb_collections = ["whiskyauctioneer_auctions"]

    category = scrapy.Field()
    end_date = scrapy.Field()
    url = scrapy.Field()
    lot = scrapy.Field()
    name = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field()
    base_info = scrapy.Field()
    intro = scrapy.Field()
    recommendations = scrapy.Field()

