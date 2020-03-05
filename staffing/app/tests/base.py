from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient

class DummyMongoDB:
    def __init__(self):
        self._params = dict()

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            self._params[name] = {'args': args, 'kwargs': kwargs}
            return self
        if name == 'inserted_id':
            return ObjectId()
        return wrapper

    def __iter__(self):
        return iter([])

    @property
    def params(self):
        return self._params

def dummy_collection(db: MongoClient):
    return DummyMongoDB()

