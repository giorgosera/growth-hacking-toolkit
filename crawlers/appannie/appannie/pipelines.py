import sys
sys.path.append("/home/george/projects/growth-hacking-toolkit/src")

from scrapy.exceptions import DropItem
from mongoengine import connect
from utils.tools import is_valid_email
from scrapy.conf import settings
from documents import AndroidApp
from mongoengine.queryset import Q

class AppanniePipeline(object):
	def __init__(self):
		db = connect(settings['MONGODB_DB'], host=settings['MONGODB_SERVER'], port=settings['MONGODB_PORT'])

	def process_item(self, item, spider):
		if item['email'] and not is_valid_email(item['email']): 
			raise DropItem("DROPPING ITEM: Developer's email address was not a valid one: %s" % item['email'])
		elif not item['email'] and not item['developer_website']: 
			raise DropItem("DROPPING ITEM: Couldn't find a valid email or website for this developer: %s" % item['name'])
		else:	
			results = AndroidApp.objects(Q(email=item['email']) | Q(company=item['company']))
			if len(results) > 0:
				raise DropItem("DROPPING ITEM: Duplicate developer was found: %s" % item['email'])
			else:			
				app = AndroidApp()
				app.name = item['name']
				app.category = item['category']
				app.company = item['company']
				app.email = item['email']
				app.developer_website = item['developer_website']
				app.min_downloads = item['min_downloads']
				app.max_downloads = item['max_downloads']
				app.is_free = item['is_free']
				app.store_url = item['store_url']
				app.save()
				return item