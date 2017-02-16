# coding: utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import requests
import settings
import os
import json
from items import *

class MeishitianxiaPipeline(object):
    def __init__(self):
        self.db = pymysql.connect("localhost","root","","cate" ,charset="utf8")
        self.cursor  = self.db.cursor()

    def process_item(self, item, spider):
        sql = ''
        if isinstance(item,foodRecommend):
            sql = "INSERT INTO `food_recommand` VALUES (\"%s\", \"%s\", \"%s\")" % (item["ingredient1"],item["ingredient2"],item["description"])
        elif isinstance(item,foodTaboo):
            sql = "INSERT INTO `food_taboo` VALUES (\"%s\", \"%s\", \"%s\")" % (item["ingredient1"],item["ingredient2"],item["description"])
        elif isinstance(item,IngredientItem):
            image_url = item["pic"]
            relative_path = "ingredients/%s/%s" % (item["name"],image_url.split("/")[-1])
            file_path = "%s/%s" % (settings.IMAGES_STORE,relative_path)
            dir_path = "%s/ingredients/%s" % (settings.IMAGES_STORE,item["name"])
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as handle:
                    response = requests.get(image_url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
                    sql = "INSERT INTO ingredients (pic,name,category,description,buySteps) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % (relative_path,item["name"],item["category"],item["description"],item["steps"].replace('"','\\"'))

        elif isinstance(item,FoodItem):
            urls = []
            name = item["name"]
            cover_url = item["cover"]
            relative_path = ''
            cover_relative_path = "food/%s/%s" % (item["name"],cover_url.split("/")[-1])
            file_path = "%s/%s" % (settings.IMAGES_STORE,cover_relative_path)
            dir_path = "%s/food/%s" % (settings.IMAGES_STORE,item["name"])
            urls.append({"file_path":file_path,"dir_path":dir_path,"relative_path":cover_relative_path,"url":cover_url})

            diagrams = json.loads(item["diagrams"])

            for temp in diagrams:
                url = temp["src"]
                relative_path = "food/%s/diagrams/%s" % (name, url.split("/")[-1])
                temp["src"] = relative_path
                file_path = "%s/%s" % (settings.IMAGES_STORE, relative_path)
                dir_path = "%s/food/%s/diagrams" % (settings.IMAGES_STORE, name)
                urls.append({"file_path": file_path, "dir_path": dir_path, "relative_path": relative_path,"url":url})

            for temp in item["steps"]:
                url = temp["stepImg"]
                relative_path = "food/%s/steps/%s" % (name, url.split("/")[-1])
                temp["stepImg"] = relative_path
                file_path = "%s/%s" % (settings.IMAGES_STORE, relative_path)
                dir_path = "%s/food/%s/steps" % (settings.IMAGES_STORE, name)
                urls.append({"file_path": file_path, "dir_path": dir_path, "relative_path": relative_path,"url":url})


            for url in urls:
                dir_path = url["dir_path"]
                file_path = url["file_path"]
                url = url["url"]
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as handle:
                        response = requests.get(url, stream=True)
                        for block in response.iter_content(1024):
                            if not block:
                                break
                            handle.write(block)

            sql = "INSERT INTO food (name,cover,diagrams,description,steps) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % (
            name, cover_relative_path, json.dumps(diagrams,ensure_ascii=False).replace('"', '\\"'), item["description"], json.dumps(item["steps"],ensure_ascii=False).replace('"', '\\"'))
            self.cursor.execute(sql)
            for temp in item["ingredients"]:
                try:
                    sql = "INSERT INTO food_ingredients (food,ingredients,account) VALUES (\"%s\", \"%s\",\"%s\")" % (name,temp["ingredientName"],temp["ingredientAmount"])
                    self.cursor.execute(sql)
                except:
                    sql = ''
            self.db.commit()
        if sql:
            self.cursor.execute(sql)
            self.db.commit()


        self.db.close()