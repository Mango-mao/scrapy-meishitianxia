# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FoodItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    cover = scrapy.Field()
    diagrams = scrapy.Field()
    description = scrapy.Field()
    ingredients = scrapy.Field()
    elseCategory = scrapy.Field()
    steps = scrapy.Field()
    kitchenware = scrapy.Field()


class IngredientItem(scrapy.Item):
    description = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    pic = scrapy.Field()
    steps = scrapy.Field()
    xuanGouJiQiao = scrapy.Field()
    yingYangJiaZhi = scrapy.Field()
    shiYongXiaoGuo = scrapy.Field()
    shiYongJingJi = scrapy.Field()

class foodTaboo(scrapy.Item):
    ingredient1 = scrapy.Field()
    ingredient2 = scrapy.Field()
    description = scrapy.Field()


class foodRecommend(scrapy.Item):
    ingredient1 = scrapy.Field()
    ingredient2 = scrapy.Field()
    description = scrapy.Field()


# temp

class HomeHealthItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()