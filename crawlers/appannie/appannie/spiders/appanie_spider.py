from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from appannie.items import AndroidAppItem
from scrapy.http.request import Request
from urlparse import urljoin
import sys
sys.path.append("/home/george/projects/growth-hacking-toolkit/src")
from utils.tools import is_valid_email

class AppannieSpider(BaseSpider):
	name = "appannie"
	allowed_domains = ["appannie.com"]

	def __init__(self, country="united-states", category="health-and-fitness"):
		self.start_urls = ['http://www.appannie.com/top/android/%s/application/%s/' % (country, category)]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		top_apps_table = hxs.select('//tbody[@id="storestats-top-table"]/tr')
		for row in top_apps_table:
			paid_app_link =  row.select('td[1]/span[@class="app-name"]/a/@href').extract()
			if paid_app_link:
				request = Request(urljoin("http://www.appannie.com", paid_app_link[0]), self.parse_app)
				request.meta['is_free'] = False 
				yield request

			free_app_link =  row.select('td[2]/span[@class="app-name"]/a/@href').extract()
			if free_app_link:
				request = Request(urljoin("http://www.appannie.com", free_app_link[0]), self.parse_app)
				request.meta['is_free'] = True 
				yield request

	def parse_app(self, response):
		hxs = HtmlXPathSelector(response)
		item = AndroidAppItem()

		#Retrieve app name
		item['name'] = hxs.select('//ul[@class="app_main_info"]/li[@class="app"]/span/text()').extract()[0]

		#Retrieve dev name
		item['developer_name'] = hxs.select('//ul[@class="app_info"]/li[contains(@class, "publisher")]/span/a/b/text()').extract()[0]

		#Retrieve developer's website and/or email
		side_bar = hxs.select('//div[@id="app_sidebar"]/div/div/ul')
		no_of_links = len(side_bar.select(".//li").extract())
		if no_of_links == 2:
			item['developer_website'] = side_bar.select(".//li[1]/a/@href").extract()[0]
			item['developer_email'] = side_bar.select(".//li[2]/a/@href").extract()[0].split(":")[1]
		elif no_of_links == 1:
			link = side_bar.select(".//li[1]/a/@href").extract()[0].split(":")[1]
			if is_valid_email(link):
				item['developer_website'] = None
				item['developer_email'] = link
			else:
				item['developer_website'] = link
				item['developer_email'] = None
		else:
			item['developer_website'] = None
			item['developer_email'] = None

		#Retrieve downloads
		downloads = hxs.select("//div[@class='app-box-itemlist about_app']/div/p[6]/text()").extract()[0].split("-")
		item['min_downloads'] = int(downloads[0].replace(",",""))
		item['max_downloads'] = int(downloads[1].replace(",",""))

		item['is_free'] = response.meta['is_free']

		return item