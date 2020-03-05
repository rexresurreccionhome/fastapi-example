from bson.objectid import ObjectId
from database.database import get_db
from staff import schemas
from staff import crud
from staff.schema_examples import (
    staff_role_example,
    salary_history_example,
    staff_example,
    staff_hired_example,
)
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
        cls.staff_id = ObjectId()
        cls.db = get_db()

    @classmethod
    def teardown_class(cls):
        cls.db.close()

    def test_collection(self, monkeypatch):
        col = crud.collection(self.db)
        assert isinstance(col, pymongo.collection.Collection)
        assert isinstance(col.database, pymongo.database.Database)
        assert col.database.name and col.name

    def test_staff_list(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(crud, "collection", dummy_collection)
            crud_result = crud.get_staff_list(self.db, 
                gender=GenderEnum.male,
                age_lte=(staff_example["age"] + 10),
                age_gte=staff_example["age"],
                country=staff_example["country"],
                state=staff_example["state"],
                zipcode=staff_example["zipcode"],
                profession=staff_example["profession"],
                skills=staff_example["skills"],
                email=staff_example["email"],
                operator="$and",
                skip=0,
                limit=100)
            assert isinstance(crud_result, DummyMongoDB)
            assert 'find' in crud_result.params and crud_result.params['find']

    def test_get_staff(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(crud, "collection", dummy_collection)
            crud_result = crud.get_staff(self.db, self.staff_id)
            assert isinstance(crud_result, DummyMongoDB)
            assert 'find_one' in crud_result.params and crud_result.params['find_one']

    def test_create_staff(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(crud, "collection", dummy_collection)
            staff_id = crud.create_staff(self.db, staff_example)
            assert isinstance(staff_id, ObjectId)

    def test_update_staff(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(crud, "collection", dummy_collection)
            crud_result = crud.update_staff(self.db, self.staff_id, staff_example)
            assert isinstance(crud_result, DummyMongoDB)
            assert 'update_one' in crud_result.params and crud_result.params['update_one']

    def test_delete_staff(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(crud, "collection", dummy_collection)
            crud_result = crud.delete_staff(self.db, self.staff_id)
            assert isinstance(crud_result, DummyMongoDB)
            assert 'delete_one' in crud_result.params and crud_result.params['delete_one']
