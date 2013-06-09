from scrapy.item import Item, Field

class AndroidAppItem(Item):
    name = Field()
    category = Field()
    company = Field()
    email = Field()
    developer_website = Field()
    min_downloads = Field()
    max_downloads = Field()
    store_url = Field()
    is_free = Field()
