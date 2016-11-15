# -*- coding: utf-8 -*-
import scrapy
import pdb


class VinbazarSpider(scrapy.Spider):
    name = "vinbazar"
    allowed_domains = ["vinbazar.com"]
    start_urls = [
        'http://vinbazar.com/otdykh/company?page=%s' % page for page in range(0,14)
    ]

    def parse(self, response):
        companies = response.css('.view-company-otdykh-list .views-row')
        records = {'data': []}
        for company in companies:
          record = {}
          record['title'] = company.css('.company-title a::text').extract_first()
          fields = company.css('.company-fields .company-field')
          record['address'] = fields[1].css('.company-field-value::text').extract_first()
          record['phone'] = fields[2].css('.company-field-value::text').extract_first()
          records['data'].append(record)
        yield records
