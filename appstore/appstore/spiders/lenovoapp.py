import scrapy
import re
from scrapy.selector import Selector
from appstore.items import AppstoreItem

class HuaweiSpider(scrapy.Spider):
    name = "huawei"
    allow_domians = ["huawei.com"]
    start_urls = [
	 "http://appstore.huawei.com/more/all"
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
