# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random
from scrapy_redis import get_redis
from scrapy import signals

CHANGE_PROXY_STATUS_LIST = [502, 404]

class ProxyMiddleware(object):
    r = get_redis()
    #rand_index = random.randint(0,r.llen("Proxy:host")-1)
    #proxy_host =  r.lindex("Proxy:host",rand_index)
    proxy_host =  r.rpoplpush("Proxy:host","Proxy:host")

    def process_request(self, request, spider):
        # Set the location of the proxy
            request.meta['proxy'] = self.proxy_host
            retry_times = request.meta.get('retry_times', 0)
            print "Current proxy: " + self.proxy_host + " Retry times: %d" % retry_times

            # Use the following lines if your proxy requires authentication
            proxy_user_pass = "iMissWonder-SP3: "

            # setup basic authentication for the proxy
            encoded_user_pass = base64.encodestring(proxy_user_pass)
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        print ('Remove proxy: %s, %d proxies left' % (
            proxy, self.r.llen("Proxy:host")-1))
        try:
            self.r.lrem("Proxy:host", 0, self.proxy_host)
            print "Successfully removed"
            rand_index = random.randint(0,self.r.llen("Proxy:host")-1)
            self.proxy_host =  self.r.lindex("Proxy:host",rand_index)
        except ValueError:
            pass

    '''
    def change_proxy(request):
        proxy = request.meta['proxy']
        # Change proxy here
        # Then check number of retries on the request
        # and decide if you want to give it another chance.
        # If not - return None else
        return request
    def process_exception(self, request, exception, spider):
        return_request = self.change_proxy(request)
        if return_request:
            return return_request

    def process_response(self, request, response, spider):
        if response.status in CHANGE_PROXY_STATUS_LIST:
            return_request = self.change_proxy(request)
            if return_request:
                return return_request
        return response
    '''

class ProxycrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
