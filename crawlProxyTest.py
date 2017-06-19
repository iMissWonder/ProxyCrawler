# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
#from scrapy import cmdline
#cmdline.execute("scrapy crawl ProxyTestSpider".split())
from ProxyCrawler.spiders import ProxyTestSpider
from scrapy.crawler import CrawlerRunner
runner = CrawlerRunner()

runner.crawl("ProxyTestSpider")
#runner.create_crawler("ProxyTestSpider")
