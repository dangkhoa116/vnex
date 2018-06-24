# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.selector import Selector
from vnex.items import VnexItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import DropItem

class StackSpider(Spider):
    name = "vnex"
    allowed_domains = ["https://*.vnexpress.net/"]
    start_urls = [
        
        "https://vnexpress.net/tin-tuc/the-gioi/page/1.html",
        "https://kinhdoanh.vnexpress.net/page/1.html",
        "https://giaitri.vnexpress.net/page/1.html",
        "https://thethao.vnexpress.net/page/1.html",
        "https://vnexpress.net/tin-tuc/phap-luat/page/1.html",
        "https://vnexpress.net/tin-tuc/giao-duc/page/1.html",
        "https://giadinh.vnexpress.net/page/1.html",
        "https://dulich.vnexpress.net/page/1.html",
        "https://vnexpress.net/tin-tuc/khoa-hoc/page/1.html"
    ]
    rules = (
        Rule(LinkExtractor(allow=r'tin-tuc/the-gioi/page/[1-2000].html'),
             callback="parse_item", follow=True),
        Rule(LinkExtractor(allow=r'tin-tuc/phap-luat/page/[1-2000].html'),
             callback="parse_item", follow=True),
        Rule(LinkExtractor(allow=r'tin-tuc/giao-duc/page/[1-1000].html'),
             callback="parse_item", follow=True),
        Rule(LinkExtractor(allow=r'tin-tuc/khoa-hoc/page/[1-1000].html'),
             callback="parse_item", follow=True),
        Rule(LinkExtractor(deny=(
			'.*\/cong\-dong\/hoi\-dap\/.*',
			'.*\/tin\-tuc\/cong\-dong\/.*',
			'.*\/tin\-tuc\/tam\-su\/.*',
			'.*\/tin\-tuc\/cuoi\/.*',
		), deny_domains=(
			'.*video\.vnexpress\.net.*',
			'.*ione\.vnexpress\.net.*',
			'.*raovat\.vnexpress\.net.*',
    )))
    )
    def parse(self, response):
        news = Selector(response).xpath('//section[@class="sidebar_1"]//article[@class="list_news"]')
        urls = {}
        for new in news:
            item = VnexItem()
            item['url'] = new.xpath(
                'h3[@class="title_news"]/a[1]/@href').extract()[0]
            if item['url'] in urls:
                raise DropItem('Item already in db')
            else:
                item['url'] = new.xpath(
                'h3[@class="title_news"]/a[1]/@href').extract()[0]
                item['title'] = new.xpath(
                    'h3[@class="title_news"]/a/@title').extract()[0]
                item['description'] = new.xpath(
                    'h4[@class="description"]/text()').extract()[0]
                yield item
            with open('log.csv', 'a') as f:
                f.write('\ntitle: {0},\nlink: {1},\ndescription: {2}\n'.format(item['title'], item['url'],
                item['description']))
            #print(item)
