# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pdb
import json
from markparser.storage import create_place

class MarkparserPipeline(object):
  def process_item(self, item, spider):
    create_place(item)
    return item
