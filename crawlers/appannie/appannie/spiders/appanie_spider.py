from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from appannie.items import AndroidAppItem
from scrapy.http.request import Request
from scrapy.http import FormRequest
from urlparse import urljoin
import sys
sys.path.append("/home/george/projects/growth-hacking-toolkit/src")
from utils.tools import is_valid_email

class AppannieSpider(BaseSpider):
	name = "appannie"
	allowed_domains = ["appannie.com"]

	def __init__(self, country="united-kingdom", category="application", sub_category="health-and-fitness"):
		self.start_urls = ['http://www.appannie.com/top/android/%s/%s/%s/' % (country, category, sub_category)]

	def parse(self, response):

		#Make first 
		request = Request("http://www.appannie.com/top-table/android/20130701-GB-4/?p=2-&h=8&iap=all",
								headers = {'X-Requested-With':'XMLHttpRequest'},
								callback=self.parse_extra, 
								dont_filter=True)
		yield request

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

	def parse_extra(self, response):
		hxs = HtmlXPathSelector(response)
		extra_rows = hxs.select('//tr')
		for row in extra_rows:
			paid_app_link =  row.select('td[1]/span[@class="app-name"]/a/@href').extract()
			if paid_app_link:
				request = Request(urljoin("http://www.appannie.com", paid_app_link[0]), self.parse_app)
				request.meta['is_free'] = False 
				yield request

			free_app_link =  row.select('td[2]/span[@class="app-name"]/a/@href').extract()
			if free_app_link:
				print urljoin("http://www.appannie.com", free_app_link[0])
				request = Request(urljoin("http://www.appannie.com", free_app_link[0]), self.parse_app)
				request.meta['is_free'] = True 
				yield request



	def parse_app(self, response):
		hxs = HtmlXPathSelector(response)
		item = AndroidAppItem()

		#Retrieve app name
		item['name'] = hxs.select('//ul[@class="app_main_info"]/li[@class="app"]/span/text()').extract()[0]

		#Retrieve company
		app_info = hxs.select('//ul[@class="app_info"]')
		item['company'] = app_info.select('.//li[contains(@class, "publisher")]/span/a/b/text()').extract()[0]

		#Retrieve store url
		item['store_url'] = app_info.select('.//li[contains(@class, "appstore")]/span/a/@href').extract()[0]

		#Retrieve developer's website and/or email
		side_bar_links = hxs.select('//div[@id="app_sidebar"]/div[@class="app-box-links links"]/div/ul')
		no_of_links = len(side_bar_links.select(".//li").extract())
		if no_of_links == 2:
			item['developer_website'] = side_bar_links.select(".//li[1]/a/@href").extract()[0]
			item['email'] = side_bar_links.select(".//li[2]/a/@href").extract()[0].split(":")[1]
		elif no_of_links == 1:
			link = side_bar_links.select(".//li[1]/a/@href").extract()[0].split(":")[1]
			if is_valid_email(link):
				item['developer_website'] = None
				item['email'] = link
			else:
				item['developer_website'] = link
				item['email'] = None
		else:
			item['developer_website'] = None
			item['email'] = None

		#Retrieve category
		item['category'] = hxs.select("//div[@class='app-box-itemlist about_app']/div/p[3]/text()").extract()[0]

		#Retrieve downloads
		downloads = hxs.select("//div[@class='app-box-itemlist about_app']/div/p[6]/text()").extract()[0].split("-")
		item['min_downloads'] = int(downloads[0].replace(",",""))
		item['max_downloads'] = int(downloads[1].replace(",",""))

		item['is_free'] = response.meta['is_free']

		return item