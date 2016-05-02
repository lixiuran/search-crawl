#coding=utf-8
import re
import json
from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.linkextractors import LinkExtractor as sle
from cnblogs.items import *

class CnblogsSpider(CrawlSpider):
    #定义爬虫的名称
    name = "CnblogsSpider"
    #定义允许抓取的域名,如果不是在此列表的域名则放弃抓取
    allowed_domains = ["www.cnblogs.com"]
    #定义抓取的入口url
    start_urls = [
        "http://www.cnblogs.com/",
        "http://www.cnblogs.com/expert/",
        "http://www.cnblogs.com/AllBloggers.aspx",
    ]
    # 定义爬取URL的规则，并指定回调函数为parse_item
    rules = [
        Rule(sle(allow=("/cate/(.*)")),follow=True),
        Rule(sle(allow=("/(.*)/category/(\d+)\.html")),follow=True),
        Rule(sle(allow=("/[a-zA-Z0-9-]{4,}/(.*?)")),follow=True,callback='parse_item'),
        Rule(sle(allow=("/[a-zA-Z0-9-]{4,}/default.html\?page=\d{1,}")),follow=True,callback='parse_item')
    ]
    print "**********CnblogsSpider**********"
    #定义回调函数
    #提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
    def parse_item(self, response):
        #print "-----------------"
        items = []
        #sel = Selector(response)
        base_url = get_base_url(response)
        postTitle = response.css('div.day div.postTitle')
        #print "=============length======="
        postCon = response.css('div.c_b_p_desc')
        postDesc = response.css('div.day div.postDesc')
        #标题、url和描述的结构是一个松散的结构，后期可以改进
        for index in range(len(postTitle)):
            item = CnblogsItem()
            item['title'] = postTitle[index].css("a").xpath('text()').extract()[0]
            #print item['title'] + "***************\r\n"
            item['link'] = postTitle[index].css('a').xpath('@href').extract()[0]
            item['list_url'] = base_url
            try:
                item['desc'] = postCon[index].xpath('text()').extract()[0]
            except Exception:
                item['desc'] = ''
            try:
                tmp = postDesc[index].xpath('text()').extract()[0]
                arr = tmp.split(' ')
                item['post_time'] = arr[2]+' '+arr[3] + ':00'
                item['post_author'] = arr[4]

                m = re.match(r".*\((\d+)\).*", arr[5])
                item['view_count'] = m.group(1)

                m2 = re.match(r".*\((\d+)\).*", arr[6])
                item['comment_count'] = m2.group(1)
            except Exception:
                print 123
            #print base_url + "********\n"
            items.append(item)
            #print repr(item).decode("unicode-escape") + '\n'
        return items
