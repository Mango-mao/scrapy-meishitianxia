# -*- coding: utf-8 -*-
import scrapy
from meishitianxia.items import *
from scrapy.shell import inspect_response
from scrapy.http import Request
import re
import json

class IngredientsSpider(scrapy.Spider):
    name = "Ingredients"
    allowed_domains = ["http://www.meishichina.com/","www.meishichina.com","home.meishichina.com"]
    start_urls = (
        'http://www.meishichina.com/YuanLiao/',
    )

    def parse(self, response):
        # inspect_response(response, self)
        categoryDivs = response.xpath("/html/body/div[5]/div/div/div")
        for categoryDiv in categoryDivs:
            category = categoryDiv.xpath("h3/text()")[0].extract()
            contents = categoryDiv.xpath("ul/li")
            for item in contents:
                url = item.xpath("a/@href").extract()[0]
                name = item.xpath("a/text()").extract()[0]
                return Request(url=url,meta={"category":category,"name":name},callback=self.parseIngredient)


    # http://www.meishichina.com/YuanLiao/JiRou/
    def parseIngredient(self, response):
        ingredient = IngredientItem()
        ingredientName = response.meta["name"]
        ingredientCategory = response.meta["category"]
        list = response.xpath("/html/body/div[6]/div/div[1]/div[2]/ul/li")
        urlRenShiYuXuanGou = response.xpath("//div[@class='ui_title_wrap clear ']/h2[2]/a/@href")[0].extract()
        urlShiYongYiJi = response.xpath("//div[@class='ui_title_wrap clear ']/h2[3]/a/@href")[0].extract()
        urlYingYangGongXiao = response.xpath("//div[@class='ui_title_wrap clear ']/h2[4]/a/@href")[0].extract()

        ingredient["name"] = ingredientName
        ingredient["category"] = ingredientCategory


        # return Request(url=urlYingYangGongXiao, meta={"ingredientName":ingredientName},callback=self.parseIngredientYingYangGongXiao)
        # return Request(url=urlShiYongYiJi, meta={"ingredientName":ingredientName},callback=self.parseIngredientShiYongYiJi)
        # return Request(url=urlRenShiYuXuanGou,meta={"item":ingredient},callback=self.parseIngredientRenShiYuXuanGou)

        for CaiPu in list:
            url = CaiPu.xpath("a[1]/@href")[0].extract()
            name = CaiPu.xpath("a/p/text()")[0].extract()
            cover = CaiPu.xpath("a/i/img/@data-src")[0].extract()
            yield Request(url=url,meta={"name":name,"cover":cover},callback=self.parseFood)


    def parseIngredientYingYangGongXiao(self, response):
        # 待学习
        inspect_response(response, self)



    def parseIngredientShiYongYiJi(self, response):
        ingredientName = response.meta["ingredientName"]
        listFoodRecommand = response.xpath("//div[@class='yiji clear mt20'][1]/ul/li")
        listFoodTaboo = response.xpath("//div[@class='yiji clear mt20'][2]/ul/li")
        for item in listFoodRecommand:
            retItem = foodRecommend()
            retItem["ingredient1"] = ingredientName
            retItem["ingredient2"] = item.xpath("div/a[1]/text()")[0].extract()
            retItem["description"] = item.xpath("p/text()")[0].extract()
            yield retItem

        for item in listFoodTaboo:
            retItem = foodTaboo()
            retItem["ingredient1"] = ingredientName
            retItem["ingredient2"] = item.xpath("div/a[1]/text()")[0].extract()
            retItem["description"] = item.xpath("p/text()")[0].extract()
            yield retItem


    def parseIngredientRenShiYuXuanGou(self, response):
        item = response.meta["item"]
        item["pic"] = response.xpath("//div[@class='blog_message']/p/img/@src")[0].extract()
        item["description"] = response.xpath("//p[@class='collect_txt mt10']/text()")[0].extract()
        item["steps"] = json.dumps(response.xpath("//div[@class='blog_message']/p/text()").extract(),encoding="UTF-8",ensure_ascii=False,indent=1)
        yield item

    def parseFood(self,response):
        food = FoodItem()
        name = response.meta["name"]
        cover = response.meta["cover"]
        thumbnailsStr = response.xpath("/html/body/div[5]/div/div[1]/div[2]/div/script/text()").extract()[0]
        thumbnails = re.findall("J_photo = (\[\S+\])",thumbnailsStr)[0]
        description = response.xpath('//*[@id="block_txt"]')[0].xpath('string(.)')[0].extract()
        listIngredients = response.xpath("//div[@class='recipeCategory_sub_R clear']/ul/li")
        listElseCategory = response.xpath("//div[@class='recipeCategory_sub_R mt30 clear']/ul/li")
        listSteps = response.xpath("//div[@class='recipeStep']/ul/li")
        kitchenware = re.findall(u"\u4f7f\u7528\u7684\u53a8\u5177\uff1a(?:(\S*)\u3001)?(\S+)\u3001?",response.xpath("//div[@class='recipeTip mt16']/text()")[0].extract())[0]

        ingredients = []

        for ingredient in listIngredients:
            ingredientName = ingredient.xpath("span[@class='category_s1']//b/text()")[0].extract()
            ingredientAmount = ingredient.xpath("span[@class='category_s2']/text()")[0].extract()
            ingredients.append({"ingredientName":ingredientName,"ingredientAmount":ingredientAmount})


        elseCategory = []

        for itemCategory in listElseCategory:
            categoryName = itemCategory.xpath("span[@class='category_s1']/a/text()")[0].extract()
            categoryAmount = itemCategory.xpath("span[@class='category_s2']/text()")[0].extract()
            elseCategory.append({"categoryName":categoryName,"categoryAmount":categoryAmount})


        steps = []

        for i in range(len(listSteps)):
            stepImg = response.xpath("//div[@class='recipeStep_img']/img/@src")[i].extract()
            stepNum = response.xpath("//div[@class='recipeStep_word']/div[@class='recipeStep_num']/text()")[i].extract()
            stepWord = response.xpath("//div[@class='recipeStep_word']/text()")[i].extract()
            steps.append({"stepImg":stepImg,"stepNum":stepNum,"stepWord":stepWord})

        food["name"] = name
        food["category"] = scrapy.Field()
        food["cover"] = cover
        food["diagrams"] = thumbnails
        food["description"] = description
        food["ingredients"] = ingredients
        food["elseCategory"] = elseCategory
        food["steps"] = steps
        food["kitchenware"] = kitchenware
        return food