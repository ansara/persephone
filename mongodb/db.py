import os
import urllib

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from dotenv import load_dotenv

load_dotenv()
USER = urllib.parse.quote_plus(os.environ['MONGO_USER'])
PASSWORD = urllib.parse.quote_plus(os.environ['MONGO_PASSWORD'])
PORT = urllib.parse.quote_plus(os.environ['MONGO_PORT'])
HOST = urllib.parse.quote_plus(os.environ['MONGO_HOST'])

class DB:

    def __init__(self):
        self.connection = self.connect_db()

    def connect_db(self):
        print("Connecting to MongoDB")
        
        try:
            client = MongoClient(f'mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/persephonedb').persephonedb

            print(f"Successfully connected to persephonedb as {USER}")

            return client
        except ConnectionFailure as err:
            print("Unable to connect to database.")

    def insert_thread(self, thread):

        thread_collection = self.connection[thread["location"]]['threads']

        try:
            existing_thread = thread_collection.find_one(
                {"url": thread["url"]}
            )

            # thread already has been tracked, just add new comments
            if existing_thread:
                thread_collection.update_one(
                    {"url": thread["url"]},
                    {"$addToSet": {"comments": thread["comments"]}},
                )
                print("Successfully added new comment to existing thread")

            else:
                thread_collection.insert_one(dict(thread))
                print("Successfully added new thread to db")
        
        except Exception as e:
            print("Error inserting thread to db: " + str(e))

    def test_db(self):
        db = self.connect_db()

        print(f"TEST: Number of Objects in CAN Collection:   {db.can.estimated_document_count()}")
        print(f"TEST: Anonme Object Fields:   {db.can.find_one({}).keys()}")
        # db.can.find_one({"url":"https://anonme.tv/can/res/3526.html"}) --> query a specific thread using url or _id
        print(f'TEST: Comment Object Fields:   {db.can.find_one({})["comments"][0].keys()}')