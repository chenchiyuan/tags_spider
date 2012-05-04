# -*- coding:utf-8 -*-
__author__ = 'chenchiyuan'

from scrapy.contrib.spiders import CrawlSpider
from models import Tag, START, END
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
import time
import re
TOTAL_NUM = 4587744

pattern = "/view/([0-9]+).htm.*"
DOMAIN = 'http://baike.baidu.com'

class Spider(CrawlSpider):
    name = 'baike'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['http://baike.baidu.com/view/1.htm']

    def parse(self, response):
        nums = Tag.remain_items()
        for i in nums:
            request_url = DOMAIN + '/view/' + str(i) + '.htm'
            request = Request(request_url, callback=self.parse_page)
            request.meta['view_num'] = str(i)
            yield request
            time.sleep(0.1)

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//h1[@class="title"]/text()').extract()
        if title and isinstance(title, list):
            title = title[0]

        url = response.url
        tags = hxs.select('//dl[@id="viewExtCati"]/dd/a/text()').extract()
        items = hxs.select('//dd[@class="relative"]/div/a/@href').extract()
        try:
            pattern_items = [re.search(pattern, item) for item in items]
            related_items = [item.group(1) for item in pattern_items if item]
        except Exception as err:
            print(err)
            return
        try:
            num = response.request.meta['view_num']
        except Exception as err:
            print(err)
            return

        tag = Tag(name=title, url=url, num=num, tags=tags, related_items=related_items)
        try:
            print("parse title %s, view num: %s" %(title, num))
            tag.save()
        except Exception as err:
            print(err)
            return

#        print("parse title %s, exist: %s" %(title, exist))
#        if exist:
#            return
#
#        more_urls = hxs.select('//dd[@class="relative"]/div/a/@href').extract()
#        for next in more_urls:
#            request_url = DOMAIN + next
#            request = Request(request_url, callback=self.parse)
#            yield request
