# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class MongoPipeline:

    def __init__(self, mongo_host, mongo_password, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_password = mongo_password
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_DB_HOST'),
            mongo_password=crawler.settings.get('MONGO_DB_PASSWORD'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_host)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if 'author' in adapter.keys():
            self.db['authors'].insert_one({
                'name': adapter['author'],
                'born_date': adapter.get('born_date', ''),
                'born_location': adapter.get('born_location', ''),
                'description': adapter.get('description', '')
            })

        if 'quote' in adapter.keys():
            self.db['quotes'].insert_one({
                'quote': adapter['quote'],
                'keywords': adapter.get('keywords', []),
                'author': adapter.get('author', '')
            })

        return item
