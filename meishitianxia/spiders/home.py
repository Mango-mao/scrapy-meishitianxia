# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from meishitianxia.items import *

class HomeSpider(scrapy.Spider):
    name = "home"
    allowed_domains = ["basic"]
    start_urls = (
        'http://www.meishichina.com/',
    )

    def parse(self, res):
        inspect_response(res,self)



    def parseArticle(self,res):
        return