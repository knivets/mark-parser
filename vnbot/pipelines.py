# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pdb
import json
from .storage import get_session, Place

class VnbotPipeline(object):
	def open_spider(self, spider):
		self.session = get_session()

	def close_spider(self, spider):
		pass

	def store_item(self, item):
		record = Place(**item)
		self.session.add(record)
		self.session.commit()

	def process_item(self, item, spider):
		for row in item['data']:
			record = row
			record['title_ru'] = row['title']
			record['title_ua'] = row['title']
			del record['title']
			self.store_item(record)
		return item
