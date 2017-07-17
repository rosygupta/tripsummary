# -*- coding: utf-8 -*-
import scrapy
from tripsummary.items import BlogItem
from scrapy import Selector
# import ipdb
import re

class BlogSpider(scrapy.Spider):
	name = 'BlogSpider'
	# start_urls = ['http://theblondeabroad.com/2017/02/16/visiting-robot-restaurant-in-tokyo/']


	def parse(self, response):
		# ipdb.set_trace()
		items = BlogItem()
		#find the heading
		heading = response.xpath('//div[@class="post-content"]//h2/text()').extract_first()
		items['heading'] = heading
		blog_text = []
		
		possible_money = ['$','£','$','¥','₹','€','million','billion','hundred','thousand','yen','dollar','euro','pound','rupee','USD']

		for cnt, h1 in enumerate(response.xpath('//div[@class="post-content"]//h1'), start=1):
			max_count = len(response.xpath('//div[@class="post-content"]//h1'))
			dict1 = {}
			#sub heading in the post
			dict1['sub_heading'] = h1.xpath('./text()').extract()[0]
			if cnt != max_count:
				#find description per section
				dict1['description'] = h1.xpath('./following::node()[count(preceding::h1)=%d][not(self::h1)]/descendant::text()' % cnt).extract()
				#find images per section
				dict1['images'] = h1.xpath('./following::img/@src[count(preceding::h1)=%d]' %cnt).extract()
			else:
				#description for the last section
				dict1['description'] = h1.xpath('./following-sibling::node()[count(preceding-sibling::h2)=1][not(self::h1)]/descendant::text()').extract()
				#images for the last section
				dict1['images'] = h1.xpath('./following::img/@src[count(preceding::h2)=2]').extract()

			dict1['description'] = ''.join(dict1['description'])

			#find the money involved phrases
			money_spent = re.findall(r"([£$¥₹€]?[\s]?[\d.,]+[\s]?)(million|billion|hundred|thousand)?[\s]?(yen|dollar|euro|pound|rupee|USD|usd)?",dict1["description"])
			#remove empty tuples
			money_spent = [tuple(filter(None, i)) for i in money_spent]
			#remove spaces by stripping
			money_spent = tuple(tuple(b.strip() for b in a) for a in money_spent)
			money_spent = [' '.join(k) for k in money_spent]
			valid_money_spent = []
			#check if the regex result is a money phrase or a random number
			for i in money_spent: 
				for k in possible_money: 
					if k.decode('utf8') in i: 
						valid_money_spent.append(i)
						break
			dict1['money_spent_phrases'] = []
			#find the corresponding line in which the money phrase was found
			for line in dict1['description'].split('. '):
				for money in valid_money_spent:
					if money in line:
						dict1['money_spent_phrases'].append({money: line})

			blog_text.append(dict1)

		items['blog_text'] = blog_text
		yield items