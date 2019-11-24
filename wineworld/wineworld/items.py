# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WineItem(scrapy.Item):
    """酒款
    """
    mongodb_spiders = ["wine"]
    mongodb_collections = ["wineworld_wine"]

    chateau = scrapy.Field()   # 酒庄
    area = scrapy.Field()    # 产区 
    area_full = scrapy.Field()    # 产区 
    url = scrapy.Field()  
    id = scrapy.Field()
    cname = scrapy.Field()
    ename = scrapy.Field()
    cover = scrapy.Field()

    logo = scrapy.Field()
    summary = scrapy.Field()
    wine_taste = scrapy.Field()
    grapes = scrapy.Field()    # 葡萄
    vintages = scrapy.Field()   # 年份


class VintAgeItem(scrapy.Item):
    """年份
    """
    mongodb_spiders = ["wine"]
    mongodb_collections = ["wineworld_vintage"]

    vintageid = scrapy.Field()  # 年份id
    wineid = scrapy.Field()   # 酒款id
    grape = scrapy.Field()
    price = scrapy.Field()
    year = scrapy.Field()
    logo = scrapy.Field()
    taste = scrapy.Field()


class ChateauItem(scrapy.Item):
    """酒庄
    """
    mongodb_spiders = ["wine"]
    mongodb_collections = ["wineworld_chateau"]

    cname = scrapy.Field()    # 中文名
    ename = scrapy.Field()    # 英文名
    img = scrapy.Field()
    brief_intro = scrapy.Field()     # 简介
    wines = scrapy.Field()    # 酒庄酒款
    infos = scrapy.Field()   # 土壤类型

