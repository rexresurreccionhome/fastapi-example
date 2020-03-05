from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
import os

#TODO: Store db info somewhere safe
CLUSTER0_CONNECT = "mongodb+srv://%s:%s@cluster0-xyz.mongodb.net/test?retryWrites=true&w=majority"
USERNAME = os.environ.get("STAFFING_USERNAME", "someuser")
PASSWORD = os.environ.get("STAFFING_USERNAME", "somepass")


def get_db():
    try:
        URI = CLUSTER0_CONNECT % (quote_plus(USERNAME), quote_plus(PASSWORD))
        db = MongoClient(URI)
        return db
    except Exception as e:
        print(e) #log error
    finally:
        db.close()


