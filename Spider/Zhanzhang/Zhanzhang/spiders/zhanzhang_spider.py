# -*- coding: utf-8 -*-
import scrapy
from Zhanzhang.items import ZhanzhangItem

class ZhanzhangSpiderSpider(scrapy.Spider):
    # 爬虫名字
    name = 'zhanzhang_spider'
    # 允许的域名
    allowed_domains = ["top.chinaz.com/"]
    # 入口url，扔到调度器
    start_urls = ["http://top.chinaz.com/hangye/index_jiaoyu_5.html/"]

    def parse(self, response):
        item_list = response.xpath("//ul[@class = 'listCentent']//li")
        for i_item in item_list:
            zhanzhang_item = ZhanzhangItem()
            zhanzhang_item['serial_number'] = i_item.xpath(
                ".//div[@class = 'RtCRateWrap']/div[@class ='RtCRateCent']/strong/text()").extract_first()
            zhanzhang_item['company_name'] = i_item.xpath(".//div[@class = 'CentTxt']/h3[@class = 'rightTxtHead']/a[@class = 'pr10 fz14']/text()").extract_first()
            zhanzhang_item['company_url'] = i_item.xpath(".//div[@class = 'CentTxt']/h3/span/text()").extract_first()
            zhanzhang_item['alexa_rank'] = i_item.xpath(".//div[@class = 'CentTxt']/div[@class = 'RtCPart clearfix']/p[@class = 'RtCData']/a[@target = '_blank']/text()").extract_first()
            zhanzhang_item['score'] = i_item.xpath(".//div[@class = 'RtCRateWrap']/div[@class ='RtCRateCent']/span/text()").extract_first()
            zhanzhang_item['verb'] = i_item.xpath(".//div[@class = 'CentTxt']/div[@class = 'RtCPart clearfix']/p[@class = 'RtCData']/a[@target = '_blank']/text()").extract()[1]
            zhanzhang_item['web_info'] = i_item.xpath(".//div[@class = 'CentTxt']/p[@class = 'RtCInfo']/text()").extract_first()
            yield zhanzhang_item
        next_link = response.xpath("//div[@class = 'ListPageWrap']/a/@href").extract()
        if next_link:
            next_link = next_link[-1]
            # print(next_link[-1])
        # print(scrapy.Request("http://top.chinaz.com/hangye" + str(next_link[-1])))
            yield scrapy.Request("http://top.chinaz.com/hangye/" + next_link, callback=self.parse, dont_filter=True)
        # print("http://top.chinaz.com/hangye/" + next_link[2])

