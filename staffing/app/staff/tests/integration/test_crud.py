from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from database.database import get_db
from staff import crud
from staff.schema_examples import staff_example
from staff.enums import  Gender as GenderEnum
import pymongo

class TestSchema:

    def setup_method(self, method):
        self.staff_id = None
        self.staff_example = staff_example.copy()
        self.db = get_db()

    def teardown_method(self, method):
        if self.staff_id:
            crud.delete_staff(self.db, self.staff_id)
        self.db.close()

    def test_1_collection(self):
        col = crud.collection(self.db)
        assert isinstance(col, pymongo.collection.Collection)
        assert isinstance(col.database, pymongo.database.Database)
        assert col.database.name and col.name

    def test_2_create_staff(self):
        self.staff_id = crud.create_staff(self.db, self.staff_example)
        assert isinstance(self.staff_id, ObjectId)

    def test_3_get_staff(self):
        self.staff_id = crud.create_staff(self.db, self.staff_example)
        crud_result = crud.get_staff(self.db, self.staff_id)
        assert isinstance(crud_result, dict)
        assert crud_result['_id'] == self.staff_id

    def test_4_update_staff(self):
        self.staff_id = crud.create_staff(self.db, self.staff_example)
        self.staff_example["name"] = "Poison Ivy"
        self.staff_example["age"] = 29
        self.staff_example["gender"] = GenderEnum.female
        self.staff_example["profession"] = "IT Specialist"
        self.staff_example["email"] = "poison.ivy@example.com"
        crud_result = crud.update_staff(self.db, self.staff_id, self.staff_example)
        assert crud_result.matched_count > 0

    def test_5_staff_list(self):
        self.staff_id = crud.create_staff(self.db, self.staff_example)
        crud_result = crud.get_staff_list(self.db, 
            gender=self.staff_example['gender'],
            age_lte=(self.staff_example["age"] + 10),
            age_gte=self.staff_example["age"],
            country=self.staff_example["country"],
            state=self.staff_example["state"],
            zipcode=self.staff_example["zipcode"],
            profession=self.staff_example["profession"],
            skills=self.staff_example["skills"],
            email=self.staff_example["email"],
            operator="$and",
            skip=0,
            limit=1)
        assert isinstance(crud_result, pymongo.cursor.Cursor)
        assert len(list(crud_result)) > 0

    def test_6_delete_staff(self):
        staff_id = crud.create_staff(self.db, self.staff_example)
        crud_result = crud.delete_staff(self.db, staff_id)
        assert crud_result.deleted_count > 0
