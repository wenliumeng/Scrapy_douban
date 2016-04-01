# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader,Identity

from doubanmoive.items import DoubanmoiveItem
from doubanmoive.items import DoubanbookItem
import os

#D:\WEB\Python\doubanmoive Scrapy crawl doubanmoive -o xxx.json   top250的详细信息 使用pipelines中的DoubanmoivePipeline1在setting中配置（存不存数据库只取决于放不放pipline，注意豆瓣有没有更新界面）
#D:\WEB\Python\doubanmoive Scrapy crawl newbook         下载新书的图片    使用pipelines中的DoubanmoivePipeline在setting中配置

class MoiveSpider(CrawlSpider):
    name="doubanmoive"
    allowed_domains=["movie.douban.com"]
    start_urls=["http://movie.douban.com/top250"]
    rules=[
        #Rule(LinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*'))),
        Rule(LinkExtractor(allow=(r'http://movie.douban.com/top250\?start=10'))),
        Rule(LinkExtractor(allow=(r'http://movie.douban.com/subject/\d+')),callback="parse_item"),
    ]

    def parse_item(self,response):
        sel=Selector(response)
        item=DoubanmoiveItem()
        item['name'] = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score']=sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        item['director']=sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['classification']= sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor']= sel.xpath('//*[@id="info"]/span[3]/a[1]/text()').extract()
        return item


class NewBookSpider(CrawlSpider):
    name="newbook"
    allowed_domains=["book.douban.com"]
    start_urls=["http://book.douban.com/latest?icn=index-latestbook-all"]
    rules=[
        Rule(LinkExtractor(allow=(r'https://book.douban.com/latest?icn=index-latestbook-all'))),
        Rule(LinkExtractor(allow=(r'https://book.douban.com/subject/\d+')), callback="parse_item"),
        # Rule(LinkExtractor(allow=r'http://book.douban.com/subject/26673089'), callback="parse_item"),
    ]

    def parse_item(self, response):
        sel = Selector(response)
        item = DoubanbookItem()
        # item = ItemLoader(item=DoubanbookItem(),response=response)
        # item.add_xpath('name',"//*[@id='mainpic"]/a/img/@src")
        item['name'] = sel.xpath('//*[@id="wrapper"]/h1/span/text()').extract()
        item['images'] = sel.xpath('//*[@id="mainpic"]/a/img/@src').extract()
        item['author'] = sel.xpath('//*[@id="info"]/span[1]/a/text()').extract()
        item['publisher'] = sel.xpath(u'//span[.//text()[normalize-space(.)="出版社:"]]/following::text()[1]').extract()
        item['publisher_year'] = sel.xpath(u'//span[.//text()[normalize-space(.)="出版年:"]]/following::text()[1]').extract()
        item['original_name'] = sel.xpath(u'//span[.//text()[normalize-space(.)="原作名:"]]/following::text()[1]').extract()
        item['translator'] = sel.xpath(u'//span[.//text()[normalize-space(.)="译者"]]/following::text()[2]').extract()
        item['page_number'] = sel.xpath(u'//span[.//text()[normalize-space(.)="页数:"]]/following::text()[1]').extract()
        item['price'] = sel.xpath(u'//span[.//text()[normalize-space(.)="定价:"]]/following::text()[1]').extract()
        item['binding'] = sel.xpath(u'//span[.//text()[normalize-space(.)="丛书:"]]/following::text()[2]').extract()
        item['series'] = sel.xpath(u'//span[.//text()[normalize-space(.)="装帧:"]]/following::text()[1]').extract()
        item['ISBN'] = sel.xpath(u'//span[.//text()[normalize-space(.)="ISBN:"]]/following::text()[1]').extract()
        item['score'] = sel.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()').extract()
        item['evaluate_number'] = sel.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/span/text()').extract()
        item['one_star'] = sel.xpath('//*[@id="interest_sectl"]/div/span[2]/text()').extract()
        item['two_star'] = sel.xpath('//*[@id="interest_sectl"]/div/span[4]/text()').extract()
        item['three_star'] = sel.xpath('//*[@id="interest_sectl"]/div/span[6]/text()').extract()
        item['four_star'] = sel.xpath('//*[@id="interest_sectl"]/div/span[8]/text()').extract()
        item['five_star'] = sel.xpath('//*[@id="interest_sectl"]/div/span[10]/text()').extract()
        return item
