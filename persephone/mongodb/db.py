import os
import ssl
import urllib

import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from dotenv import load_dotenv

load_dotenv()
USER = os.environ["MONGO_USER"]
PASSWORD = os.environ["MONGO_PASSWORD"]

def connect_db():
    print("Connecting to MongoDB")
    user = urllib.parse.quote_plus(USER)
    password = urllib.parse.quote_plus(PASSWORD)

    try:
        client = MongoClient(
            f'mongodb://{user}:{password}@localhost:27017/',
            ssl=True,
            ssl_cert_reqs=ssl.CERT_NONE,
        )

        print("Successfully connected to database")
        return client
    except ConnectionFailure as err:
        print("Unable to connect to database.")


def test_db():
    db = connect_db()

    print(
        f"TEST: Number of Objects in CAN Collection:   {db.can.estimated_document_count()}"
    )
    print(f"TEST: Anonme Object Fields:   {db.can.find_one({}).keys()}")
    # db.can.find_one({"url":"https://anonme.tv/can/res/3526.html"}) --> query a specific thread using url or _id
    print(f'TEST: Comment Object Fields:   {db.can.find_one({})["comments"][0].keys()}')