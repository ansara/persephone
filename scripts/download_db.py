import os
import ssl
import logging

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()
ibm_password = os.environ["IBM_CLOUD_PASSWORD"]

logging.basicConfig(level=logging.DEBUG)

try:
    client = MongoClient(
         f"mongodb://admin:{ibm_password}@f443f26c-22db-4cfc-b0db-17d6de5f58ff-0.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860,f443f26c-22db-4cfc-b0db-17d6de5f58ff-1.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860,f443f26c-22db-4cfc-b0db-17d6de5f58ff-2.c0v4phir0ah9ul9trho0.databases.appdomain.cloud:30860/ibmclouddb?authSource=admin&replicaSet=replset",
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE,
    )

    connection = client.ibmclouddb
    logging.info("Successfully connected to MongoDB")

except ConnectionFailure as err:
    logging.info("Unable to initialize connection to MongoDB")
