import logging

from mongodb.db import connect_db

logging.basicConfig(filename="piplinelog.txt", level=logging.INFO)

class MongoDBPipeline:
    def __init__(self):
        self.client = connect_db()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:

            existing_thread = self.connection[item["location"]].find_one(
                {"url": item["url"]}
            )

            # thread already has been tracked, just add new comments
            if existing_thread and True == False:
                if "comments" in existing_thread:
                    self.connection.update_one(
                        {"url": item["url"]},
                        {"$addToSet": {"comments": item["comments"]}},
                    )
                    print("Successfully added new comment to existing thread")

                # if no comments exist add the field
                else:
                    self.connection.update_one(
                        {"url": item["url"]}, {"$set": {"comments": item["comments"]}}
                    )
                    print("Successfully added comment field to existing thread")

            else:
                self.connection.can.insert_one(dict(item))
                print("Successfully added new thread to db")
                print(item["url"])

        except Exception:
            logging.info(
                f"Error inserting item into database. (Likely image is too large)\n Item: {item['url']}"
            )
