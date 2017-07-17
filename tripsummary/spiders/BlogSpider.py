# -*- coding: utf-8 -*-
import scrapy
from tripsummary.items import BlogItem
from scrapy import Selector
import ipdb
import re

class BlogSpider(scrapy.Spider):
	name = 'BlogSpider'
	# allowed_domains = ['http://theblondeabroad.com/2017/02/16/visiting-robot-restaurant-in-tokyo/']


	def parse(self, response):
		# ipdb.set_trace()
		items = BlogItem()
		heading = response.xpath('//div[@class="post-content"]//h2/text()').extract_first()
		items['heading'] = heading
		blog_text = []
		possible_money = ['$','£','$','¥','₹','€','million','billion','hundred','thousand',
		'yen','dollar','euro','pound','rupee','USD']

		for cnt, h1 in enumerate(response.xpath('//div[@class="post-content"]//h1'), start=1):
			max_count = len(response.xpath('//div[@class="post-content"]//h1'))
			dict1 = {}
			dict1['sub_heading'] = h1.xpath('./text()').extract()[0]
			if cnt != max_count:
				dict1['description'] = h1.xpath('./following::node()[count(preceding::h1)=%d][not(self::h1)]/descendant::text()' % cnt).extract()
				#find images per section
				dict1['images'] = h1.xpath('./following::img/@src[count(preceding::h1)=%d]' %cnt).extract()
			else:
				dict1['description'] = h1.xpath('./following-sibling::node()[count(preceding-sibling::h2)=1][not(self::h1)]/descendant::text()').extract()
				dict1['images'] = h1.xpath('./following::img/@src[count(preceding::h2)=2]').extract()

			dict1['description'] = ''.join(dict1['description'])

			money_spent = re.findall(r"([£$¥₹€]?[\s]?[\d.,]+[\s]?)(million|billion|hundred|thousand)?[\s]?(yen|dollar|euro|pound|rupee|USD|usd)?",dict1["description"])
			money_spent = [tuple(filter(None, i)) for i in money_spent]
			money_spent = tuple(tuple(b.strip() for b in a) for a in money_spent)
			money_spent = [' '.join(k) for k in money_spent]
			valid_money_spent = []
			for i in money_spent: 
				for k in possible_money: 
					if k.decode('utf8') in i: 
						valid_money_spent.append(i)
						break
			dict1['money_spent_phrases'] = []
			for line in dict1['description'].split('. '):
				for money in valid_money_spent:
					if money in line:
						dict1['money_spent_phrases'].append({money: line})

			blog_text.append(dict1)
		items['blog_text'] = blog_text


		yield items