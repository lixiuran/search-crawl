# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogsItem(scrapy.Item):
    # define the fields for your item here like:
    item_id  = scrapy.Field()
    title    = scrapy.Field()
    link     = scrapy.Field()
    desc     = scrapy.Field()
    list_url = scrapy.Field()
    post_time   = scrapy.Field()
    post_author = scrapy.Field()
    view_count  = scrapy.Field()
    comment_count = scrapy.Field()
    pass
