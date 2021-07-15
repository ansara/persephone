import os
import ssl
import urllib

import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from dotenv import load_dotenv

load_dotenv()
USER = urllib.parse.quote_plus(os.environ["MONGO_USER"])
PASSWORD = urllib.parse.quote_plus(os.environ["MONGO_PASSWORD"])
PORT = urllib.parse.quote_plus(os.environ['MONGO_PORT'])
HOST = urllib.parse.quote_plus(os.environ['MONGO_HOST'])

def connect_db():
    print("Connecting to MongoDB")
    
    try:
        client = MongoClient(
            f'mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/',
            ssl=True,
            ssl_cert_reqs=ssl.CERT_NONE,
        )

        print("Successfully connected to database")
        return client
    except ConnectionFailure as err:
        print("Unable to connect to database.")

#add existing data to database if data folder exists
def init_db():
    pass

def test_db():
    db = connect_db()

    print(
        f"TEST: Number of Objects in CAN Collection:   {db.can.estimated_document_count()}"
    )
    print(f"TEST: Anonme Object Fields:   {db.can.find_one({}).keys()}")
    # db.can.find_one({"url":"https://anonme.tv/can/res/3526.html"}) --> query a specific thread using url or _id
    print(f'TEST: Comment Object Fields:   {db.can.find_one({})["comments"][0].keys()}')