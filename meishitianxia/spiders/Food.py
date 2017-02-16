# -*- coding: utf-8 -*-
import scrapy


class FoodSpider(scrapy.Spider):
    name = "food"
    allowed_domains = ["basic"]
    start_urls = (
        'http://www.basic/',
    )

    def parse(self, response):
        pass
