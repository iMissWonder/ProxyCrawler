# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from scrapy.http import Request

class ProxyTestSpider(scrapy.Spider):
    name = "ProxyTestSpider"
    start_urls = ['http://icanhazip.com/']
    def parse(self, response):
        current_proxy = response.meta.get('proxy',0)
        selector = Selector(response)
        current_ip = selector.xpath('//p/text()').extract()
        proxy_ip = str(re.search(u'http://(.*?):', current_proxy).group(1))
        print body
        print
        #if body.find("") != -1:
        print "###### Valid IP######"
