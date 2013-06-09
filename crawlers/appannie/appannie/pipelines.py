from scrapy.exceptions import DropItem
import sys
sys.path.append("/home/george/projects/growth-hacking-toolkit/src")
from utils.tools import is_valid_email

class AppanniePipeline(object):
	def __init__(self):
		self.existing_developer_emails = set()

	def process_item(self, item, spider):
		if item['developer_email'] and item['developer_email'] in self.existing_developer_emails:
			raise DropItem("DROPPING ITEM: Duplicate developer email found: %s" % item['developer_email'])
		elif item['developer_email'] and not is_valid_email(item['developer_email']): 
			raise DropItem("DROPPING ITEM: Developer's email address was not a valid one: %s" % item['developer_email'])
		elif not item['developer_email'] and not item['developer_website']: 
			raise DropItem("DROPPING ITEM: Couldn't find a valid email or website for this developer: %s" % item['name'])
		else:
			return item