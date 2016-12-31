# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from markparser.items import PlaceItem
import base64
import unicodedata
import re
import pdb

def extract_title_and_kind(string):
  # extract kind from title
  # we match the reverse of the string because we want to
  # search right to left. An example of a matched string is
  # (something)
  matcher = re.compile('\)[^)(]+\( ')
  kind = None
  # removing whitespace from the right otherwise our match might fail
  # then reversing the string to facilitate right to left match
  reverse = string.rstrip()[::-1]
  result = matcher.match(reverse)
  if result:
    # reversing back, stripping space and parenthesis
    kind = result.group(0)[::-1].lstrip()[1:-1]
  # removing kind from the end of the title and reversing
  title = matcher.sub('', reverse, count=1)[::-1]
  return (title, kind)

def extract_city_and_address(string):
  # й here is a hack -- i'm not sure what encoding the original letter has
  # decided to not use for now
  matcher = re.compile(r'г\. [\wй ]*\,')
  city = None
  address_s = ' '.join(string.split()) # removing multiple whitespace
  coms = address_s.split(',')
  # grabbing 1st elem from address string
  # removing 'г. '
  city_s = coms[0][3:]
  # if string is not empty after this
  # then we have a city
  if city_s:
    city = city_s

  address = (','.join(coms[1:])).strip()
  return (address, city)

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
        title = item_sel.css('a.catHeader::text').extract_first()
        if title:
          record['title'], kind = extract_title_and_kind(title)
          if kind:
            record['kind'] = kind
        address = item_sel.css('div.infoBlock::text').extract_first()
        if address.strip():
          record['address'], city = extract_city_and_address(address)
          if city:
            record['city'] = city
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
