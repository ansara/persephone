import logging
import os
import ssl

import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()
password = os.environ["IBM_CLOUD_PASSWORD"]
logging.basicConfig(filename="piplinelog.txt", level=logging.INFO)


class MongoDBPipeline:
    def __init__(self):

        try:
            self.client = MongoClient(
                f"mongodb://admin:{password}@f443f26c-22db-4cfc-b0db-17d6de5f58ff-0.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860,f443f26c-22db-4cfc-b0db-17d6de5f58ff-1.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860,f443f26c-22db-4cfc-b0db-17d6de5f58ff-2.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860/ibmclouddb?authSource=admin&replicaSet=replset",
                ssl=True,
                ssl_cert_reqs=ssl.CERT_NONE,
            )

            self.connection = self.client.ibmclouddb
            logging.info("Successfully connected to database in pipeline")

        except ConnectionFailure as err:
            logging.info("Unable to initialize connection to database in pipeline")

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
