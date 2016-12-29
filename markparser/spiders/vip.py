# -*- coding: utf-8 -*-
import scrapy
import pdb


class VipSpider(scrapy.Spider):
    name = "vip"
    allowed_domains = ["vip.vn.ua"]
    start_urls = ['http://vip.vn.ua/']
    base_url = 'http://vip.vn.ua'

    def start_requests(self):
      menus = [
        'restaurant',
        'night_clubs',
        'cafe_and_bars',
        'pub_vinnitsa',
        'karaoke_club',
        'pizza',
        'hookahbar',
        'fast_food',
        'billiard_and_bowling',
        'roledrom_vinnitsa',
        'ice_skating',
        'exstrim',
        'shoping_mall',
        'movie_theatres',
      ]
      for link in menus:
        yield scrapy.Request('http://vip.vn.ua/%s/' % link, self.parse)

    def build_url(self, url):
      return self.base_url + url

    def parse(self, response):
      # scrap and parse all items on the current page
      current = response.url.split('/')[3]
      links = response.css('a.small_link::attr(href)').extract()
      for link in links:
        if current in link:
          url = self.build_url(link)
          yield scrapy.Request(url, callback=self.parse_place)
        
      # then grab the next page and repeat
      pages_unfiltered = response.css('a.submenu::attr(href)').extract()
      pages = set()
      for page in pages_unfiltered:
        if ('%s/page' % current) in page:
          pages.add(page)
      if len(pages) > 0:
        for page in pages:
          url = self.build_url(page)
          yield scrapy.Request(url, callback=self.parse)

    def parse_place(self, response):
      address = response.xpath("//span[contains(text(),'Адрес:')]/ancestor-or-self::p/parent::td/following-sibling::td//span/text()").extract()
      response.xpath("//span[contains(text(),'Телефоны:')]/ancestor-or-self::p/parent::td/following-sibling::td//span/text()").extract()
      pass
