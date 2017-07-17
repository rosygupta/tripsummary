# -*- coding: utf-8 -*-
 
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
 
import scrapy
 
class BlogItem(scrapy.Item):
  # define the fields for your item here like:
  heading = scrapy.Field()
  sub_heading = scrapy.Field()
  blog_text = scrapy.Field()
  image_url = scrapy.Field()
  date = scrapy.Field()
  image_title = scrapy.Field()
