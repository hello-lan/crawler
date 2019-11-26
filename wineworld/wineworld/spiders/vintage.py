# -*- coding: utf-8 -*-
import scrapy
import json
import csv

from wineworld.items import VintAgeItem


class VintageSpider(scrapy.Spider):
    name = 'vintage'
    allowed_domains = ['wine-world.com']
    start_urls = []

    vintage_url = "https://m.wine-world.com/wine/GetWineInfo"

    def __init__(self, fpath=None, *args, **kwargs):
        super(VintageSpider, self).__init__(*args, **kwargs)
        self.fpath = fpath

    def start_requests(self):
        # wine_id = "ad679838-5304-4973-be95-0162fa5d2d7c"
        # vintage_id = "14e0615b-e0d5-4e12-8051-27382e1c7165"
        # data = {"wineid": wine_id, "vintageid":vintage_id}

        with open(self.fpath) as f:
            csv_reader = csv.reader(f, delimiter=",")
            for wine_id, vintage_id in csv_reader:
                data = {"wineid": wine_id, "vintageid":vintage_id}
                yield scrapy.FormRequest(self.vintage_url,
                                         formdata=data,
                                         callback=self.parse,
                                         meta={"idinfo": data}
                                        )

    def parse(self, response):
        idinfo = response.meta["idinfo"]
        jdata = json.loads(response.text)
        item = VintAgeItem()
        item["vintageid"] = idinfo["wineid"]
        item["wineid"] = idinfo["vintageid"]
        item["grape"] =  jdata["GrapeVariety"]
        item["price"] = jdata["price"]
        item["year"] = jdata["wineYear"]
        item["logo"] = jdata["winelogo"]
        item["taste"] = jdata["WineTaste"]
        return item
