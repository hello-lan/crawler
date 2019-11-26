# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request

from wineworld.items import WineItem


class WineSpider(scrapy.Spider):
    name = 'wine'
    allowed_domains = ['wine-world.com']
    start_urls = []

    wine_list_url = "https://m.wine-world.com/wine/HitWine"
    vintage_url = "https://m.wine-world.com/wine/GetWineInfo"

    custom_settings = {
        "ITEM_PIPELINES": {
            "wineworld.pipelines.MongoDBPipeline": 301,
        },
        "DOWNLOAD_DELAY": 0.8,
    }

    def start_requests(self):
        yield scrapy.FormRequest(self.wine_list_url, 
                formdata={"pageIndex": "1"},
                callback=self.parse,
                meta={"page": 1})

    def parse(self, response):
        jdata = json.loads(response.text)
        for row in jdata["rows"]:
            url = row["url"]
            yield Request(url, meta={"row": row}, callback=self.parse_item)

        page_count = jdata["pageCount"]
        page = response.meta["page"]
        if page < page_count:
            page += 1
            yield scrapy.FormRequest(
                    response.url,
                    formdata={"pageIndex": str(page)},
                    callback=self.parse,
                    meta={"page": page})

    def parse_item(self, response):
        # 酒款
        item = WineItem()
        row = response.meta["row"]
        item["url"] = row["url"]
        item["id"] = row["id"]
        item["cname"] = row["cname"]
        item["ename"] = row["fname"]
        item["area"] = row["areaName"]
        item["cover"] = row["cover"]
        item["grapes"] = row["grapeName"]

        item["logo"] = response.css("#winelogo::attr(src)").get()
        item["winery"] = response.css("ul.wine-attr > li:contains(酒庄) > .attr-r::text").get(default="").strip()
        item["area_full"] = response.css("ul.wine-attr > li:contains(产区) > .attr-r::text").get(default="").strip().replace("\xa0", '').replace(" ", "")
        item["summary"] = response.css(".summary::text").get()
        item["wine_taste"] = response.css("#WineTaste::text").get()
#        item["grapes"] = response.css("#grapeList::text").get("").strip()
        vintage_list = []
        formdatas = []
        for tmp_sel in response.css(".vtcell"):
            wineid, vintageid = tmp_sel.css("a::attr(onclick)").re("LoadData\('(.*?)','(.*?)'")
            if len(vintageid) == 0:
                continue
            year = tmp_sel.css("a::text").get("").strip()
            vintage_list.append(
                    {"wineid": wineid,
                     "vintageid": vintageid,
                     "year": year}
                    )
            formdatas.append({"wineid":wineid, "vintageid":vintageid})
        item["vintages"] = vintage_list
        yield item
