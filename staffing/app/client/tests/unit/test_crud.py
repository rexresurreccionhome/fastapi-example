from bson.objectid import ObjectId
from database.database import get_db
from client import schemas
from client import crud
from client.schema_examples import client_example
from staff.schemas import StaffHired
from staff.schema_examples import staff_hired_example
from staff.enums import (
    Gender as GenderEnum,
    Employment as EmploymentEnum,
    PayType as PayTypeEnum,
)
from tests.base import DummyMongoDB, dummy_collection
import pymongo

class TestCrud:

    @classmethod
    def setup_class(cls):
        cls.client_id = ObjectId()
        cls.db = get_db()

    @classmethod
    def teardown_class(cls):
        cls.db.close()

    def test_collection(self, monkeypatch):
        col = crud.collection(self.db)
        assert isinstance(col, pymongo.collection.Collection)
        assert isinstance(col.database, pymongo.database.Database)
        assert col.database.name and col.name

    def test_client_list(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(crud, "collection", dummy_collection)
            crud_result = crud.get_client_list(self.db, 
                company=client_example["company"],
                size_lte=(client_example["size"] + 100),
                size_gte=client_example["size"],
                country=client_example["country"],
                state=client_example["state"],
                zipcode=client_example["zipcode"],
                industry=client_example["industry"],
                services=client_example["services"],
                email=client_example["email"],
                operator="$and",
                skip=0,
                limit=100)
            assert isinstance(crud_result, DummyMongoDB)
            assert 'find' in crud_result.params and crud_result.params['find']

    def test_get_client(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(crud, "collection", dummy_collection)
            crud_result = crud.get_client(self.db, self.client_id)
            assert isinstance(crud_result, DummyMongoDB)
            assert 'find_one' in crud_result.params and crud_result.params['find_one']

    def test_create_client(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(crud, "collection", dummy_collection)
            client_id = crud.create_client(self.db, client_example)
            assert isinstance(client_id, ObjectId)

    def test_update_client(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(crud, "collection", dummy_collection)
            crud_result = crud.update_client(self.db, self.client_id, client_example)
            assert isinstance(crud_result, DummyMongoDB)
            assert 'update_one' in crud_result.params and crud_result.params['update_one']

    def test_update_staff_hired1(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(crud, "get_client", (lambda db, client_id: {"_id": client_id}))
            m.setattr(crud, "collection", dummy_collection)
            crud_result = crud.update_staff_hired(self.db, self.client_id, staff_hired_example)
            assert isinstance(crud_result, DummyMongoDB)
            assert 'update_one' in crud_result.params and crud_result.params['update_one']

    def test_update_staff_hired2(self, monkeypatch):
        hired = [StaffHired(**sh) for sh in staff_hired_example]
        with monkeypatch.context() as m:
            m.setattr(crud, "get_client", (lambda db, client_id: {"_id": client_id, "staff_hired": staff_hired_example}))
            m.setattr(crud, "collection", dummy_collection)
            crud_result = crud.update_staff_hired(self.db, self.client_id, hired)
            assert isinstance(crud_result, DummyMongoDB)
            assert 'update_one' in crud_result.params and crud_result.params['update_one']

    def test_delete_client(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(crud, "collection", dummy_collection)
            crud_result = crud.delete_client(self.db, self.client_id)
            assert isinstance(crud_result, DummyMongoDB)
            assert 'delete_one' in crud_result.params and crud_result.params['delete_one']
