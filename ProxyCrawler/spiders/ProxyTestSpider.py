# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from scrapy_redis import get_redis

class ProxyTestSpider(scrapy.Spider):
    name = "ProxyTestSpider"
    start_urls = ['http://icanhazip.com/']
    def parse(self, response):
        current_proxy = response.meta.get('proxy',0)
        selector = Selector(response)
        current_ip = selector.xpath('//p/text()').extract()
        try:
            current_ip = current_ip[0]
        except IndexError:
            self.del_proxy(current_proxy)
            print "***** InValid IP *****"
            return
        proxy_ip = str(re.search(u'http://(.*?):', current_proxy).group(1))
        print "Current ip = " + current_ip
        print "  Proxy ip = " + proxy_ip
        if current_ip == proxy_ip:
            print "###### Valid IP ######"
        else:
            self.del_proxy(current_proxy)
            print "***** Invalid IP *****"

    def del_proxy(self, current_proxy):
        r = get_redis()
        print ('Remove proxy: %s, %d proxies left' % (
            current_proxy, r.llen("Proxy:host")-1))
        r.lrem("Proxy:host", 0, current_proxy)
        print "Successfully removed :" + current_proxy

