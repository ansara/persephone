import os
import ssl

import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()
password = os.environ["IBM_CLOUD_PASSWORD"]


def connect_db():
    print("Connecting to MongoDB - IBM Cloud")
    try:
        client = MongoClient(
            f"mongodb://admin:{password}@f443f26c-22db-4cfc-b0db-17d6de5f58ff-0.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860,f443f26c-22db-4cfc-b0db-17d6de5f58ff-1.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860,f443f26c-22db-4cfc-b0db-17d6de5f58ff-2.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860/ibmclouddb?authSource=admin&replicaSet=replset",
            ssl=True,
            ssl_cert_reqs=ssl.CERT_NONE,
        )

        db = client.ibmclouddb
        return db
    except ConnectionFailure as err:
        print("Unable to connect to database.")


def test_db():
    db = connect_db()

    # Testing 'can', the the collection representing Canada
    # The image bytes are stored alongside the text so displaying items using keys

    print(
        f"TEST: Number of Objects in CAN Collection:   {db.can.estimated_document_count()}"
    )
    print(f"TEST: Anonme Object Fields:   {db.can.find_one({}).keys()}")
    # db.can.find_one({"url":"https://anonme.tv/can/res/3526.html"}) --> query a specific thread using url or _id
    print(f'TEST: Comment Object Fields:   {db.can.find_one({})["comments"][0].keys()}')
