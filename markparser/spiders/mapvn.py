# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from markparser.items import PlaceItem
import base64
import unicodedata
import pdb


class MapvnSpider(scrapy.Spider):
		name = "mapvn"
		allowed_domains = ["map.vn.ua"]
		start_urls = ['http://map.vn.ua/catalog/kultura-dosug/obshepit-kafe/']

		def parse(self, response):
			categories = response.css('div.indexCatalog1 ul li a::attr(href)').extract()
			for category in categories:
				yield scrapy.Request(category, callback=self.parse_category)
		def parse_category(self, response):
			items = response.css('div.companyInListContainer').extract()
			for item in items:
				item_sel = Selector(text=item)
				record = PlaceItem()
				record['title'] = item_sel.css('a.catHeader::text').extract_first()
				record['address'] = item_sel.css('div.infoBlock::text').extract_first()
				record['website'] = item_sel.css('div.buSite a::text').extract_first()
				phone = item_sel.css('div.phoneFade::attr(phone)').extract_first()
				if phone:
					record['phone'] = base64.b64decode(phone).decode('utf-8')
				for key, val in record.items():
					if val:
						record[key] = unicodedata.normalize('NFKD', val)
				yield record
			pages = response.css('div.companiesListPager a.pager-page::attr(href)').extract()
			for page in pages:
				yield scrapy.Request(page, callback=self.parse_category)
