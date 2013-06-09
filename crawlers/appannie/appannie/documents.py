from mongoengine import *
import datetime

class AndroidApp(Document):
	name = StringField(max_length=400, required=True)
	category = StringField(max_length=400, required=True)
	company = StringField(max_length=200, required=True)
	email = EmailField()
	developer_website = URLField()
	min_downloads = IntField(default=0)
	max_downloads = IntField(default=0)
	is_free = BooleanField(default=False)
	store_url = URLField(required=True)
	date_modified = DateTimeField(default=datetime.datetime.now)
