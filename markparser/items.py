# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlaceItem(scrapy.Item):
  title = scrapy.Field()
  address = scrapy.Field()
  phone = scrapy.Field()
  website = scrapy.Field()
  kind = scrapy.Field()
