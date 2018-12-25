# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhanzhangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 网站排名
    serial_number = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 公司网址
    company_url = scrapy.Field()
    # alexa周排名
    alexa_rank = scrapy.Field()
    # 网站评分
    score = scrapy.Field()
    # 网站反链数
    verb = scrapy.Field()
    # 网站简介
    web_info = scrapy.Field()
