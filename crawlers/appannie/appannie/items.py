from scrapy.item import Item, Field

class AndroidAppItem(Item):
    name = Field()
    developer_name = Field()
    developer_email = Field()
    developer_website = Field()
    min_downloads = Field()
    max_downloads = Field()
    has_iap = Field()
    is_free = Field()
