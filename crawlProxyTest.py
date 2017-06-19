# -*- coding: utf-8 -*-

#from scrapy import cmdline
#cmdline.execute("scrapy crawl ProxyTestSpider".split())

from scrapy.crawler import CrawlerRunner
runner = CrawlerRunner()

runner.create_crawler("ProxyTestSpider")
runner.create_crawler("ProxyTestSpider")
