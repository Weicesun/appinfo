import scrapy
import re
from scrapy.selector import Selector
from appstore.items import AppstoreItem

class HuaweiSpider(scrapy.Spider):
    name = "huawei"
    allow_domians = ["huawei.com"]
    start_urls = [
	 "http://appstore.huawei.com/more/all"
	 "http://appstore.huawei.com/more/soft"
	 "http://appstore.huawei.com/more/game"
	 "http://appstore.huawei.com/more/newPo"
	 "http://appstore.huawei.com/more/newUp"
	 "http://appstore.huawei.com/search/%25E6%2589%258B%25E6%259C%25BA%25E7%2599%25BE%25E5%25BA%25A6"
	 "http://appstore.huawei.com/search/%25E6%2594%25AF%25E4%25BB%2598%25E5%25AE%259D"
    ]
    def parse(self, respose):
		page = Selector(respose)
		hrefs = page.xpath('//h4[@class="title"]/a/@href')
		for href in hrefs:
	    	url = href.extract()
	    	yield scrapy.Request(url, self.parse_item, meta = {
	    		'splash':{
	    		'endpoint':'render.html',
	    		'args': {'wait':0.5}
	    		}
	    		})
	 
	def find_next_page(self, url):
		try:
			page_num_str = url.split('/')[-1]
			page_num = int(page_num_str) + 1
			url = url[:-len(page_num_str)] + str(page_num)   
			return url
		except ValueError:
			print "page can't handle"
			print url
			return "http://www.google.com"
    def parse_item(self, respose):
		page = Selector(respose)
		item = AppstoreItem()
		item['title'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()')\
		.extract_first().encode('utf-8')
        item['url'] = respose.url
        appid = re.match(r'http://.*/(.*)', item['url']).group(1)
        item['appid'] = appid
		item['intro'] = page.xpath('//meta[@name="description"]/@content').\
        extract_first().encode('utf-8')
        item['turl'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li[@class="img"]/img[@class="app-ico"]/@lazyload')\
		.extract_first()
		divs = page.xpath('//div[@class="open-info"]')
		recomm = ""
		for div in divs:
			url = div.xpath('./p[@class="name"]/a/@href').extract_first()
			recommended_appid = re.match(r'http://.*/(.*)', url).group(1)
			name = div.xpath('./p[@class="name"]/a/text()').\
			extract_first().encode('utf-8')
			recomm += "{0}:{1},".format(recommended_appid, name)
			item['recommended'] = recomm
			yield item
