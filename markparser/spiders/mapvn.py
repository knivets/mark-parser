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
  reverse = string.strip()[::-1]
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

def website_validator(website):
  return website and website.strip() and ('.' in website) and ('map.vn.ua' not in website)

def decode_and_format_phone(string):
  phone_s = base64.b64decode(string).decode('utf-8')
  phone_s = phone_s[3:] # remove 'т. ' 
  # removing whitespace and dashes
  phone_s = phone_s.replace(' ', '').replace('-', '').replace('&ndash;', '')
  phones = phone_s.split(',')
  fin_phones = []
  for p in phones:
    if p:
      norm_p = p
      if norm_p[0] != '+':
        # adding phone code
        norm_p = '+38' + norm_p
      if ')(' in norm_p: # removing duplicate area code
        norm_p = norm_p.replace('(0432)(0432)', '(0432)')
      fin_phones.append(norm_p)
  return ', '.join(fin_phones)

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
        address = item_sel.css('div.infoBlock::text').extract_first()
        website = item_sel.css('div.buSite a::text').extract_first()
        phone = item_sel.css('div.phoneFade::attr(phone)').extract_first()
        if title:
          title = unicodedata.normalize('NFKD', title)
          record['title'], kind = extract_title_and_kind(title)
          if kind:
            record['kind'] = kind
        if address and address.strip():
          address = unicodedata.normalize('NFKD', address)
          record['address'], city = extract_city_and_address(address)
          if city:
            record['city'] = city
        if website_validator(website):
          website = unicodedata.normalize('NFKD', website)
          record['website'] = website.strip()
        if phone:
          phone = unicodedata.normalize('NFKD', phone)
          record['phone'] = decode_and_format_phone(phone)
        yield record
      pages = response.css('div.companiesListPager a.pager-page::attr(href)').extract()
      for page in pages:
        yield scrapy.Request(page, callback=self.parse_category)
