# Scrapy settings for appannie project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'appannie'

SPIDER_MODULES = ['appannie.spiders']
ITEM_PIPELINES = ['appannie.pipelines.AppanniePipeline']
NEWSPIDER_MODULE = 'appannie.spiders'
COOKIES_ENABLED = False
DOWNLOAD_DELAY = 2.0

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "appannie"
MONGODB_COLLECTION = "android"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'appannie (+http://www.yourdomain.com)'
