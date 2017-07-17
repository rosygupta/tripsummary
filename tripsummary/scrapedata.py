from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from spiders.BlogSpider import BlogSpider
from items import BlogItem


configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()
d = runner.crawl(BlogSpider, start_urls=['http://theblondeabroad.com/2017/02/16/visiting-robot-restaurant-in-tokyo/'])
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished
