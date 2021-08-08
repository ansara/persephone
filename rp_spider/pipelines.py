import logging

from mongodb.db import DB

logging.basicConfig(filename="piplinelog.txt", level=logging.INFO)

class MongoDBPipeline:
    def __init__(self):
        self.connection = DB()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.connection.insert_thread(item)

        except Exception:
            logging.info(
                f"Error inserting item into database\n Item: {item['url']}"
            )
