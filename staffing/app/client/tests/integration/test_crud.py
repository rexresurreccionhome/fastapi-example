from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from database.database import get_db
from client import crud
from client.schema_examples import client_example
from staff.schemas import StaffHired
from staff.schema_examples import staff_hired_example
import pymongo

class TestSchema:

    def setup_method(self, method):
        self.client_id = None
        self.client_example = client_example.copy()
        self.db = get_db()

    def teardown_method(self, method):
        if self.client_id:
            crud.delete_client(self.db, self.client_id)
        self.db.close()

    def test_1_collection(self):
        col = crud.collection(self.db)
        assert isinstance(col, pymongo.collection.Collection)
        assert isinstance(col.database, pymongo.database.Database)
        assert col.database.name and col.name

    def test_2_create_client(self):
        self.client_id = crud.create_client(self.db, self.client_example)
        assert isinstance(self.client_id, ObjectId)

    def test_3_get_client(self):
        self.client_id = crud.create_client(self.db, self.client_example)
        crud_result = crud.get_client(self.db, self.client_id)
        assert isinstance(crud_result, dict)
        assert crud_result['_id'] == self.client_id

    def test_4_update_staff(self):
        self.client_id = crud.create_client(self.db, self.client_example)
        self.client_example["company"] = "IT Worx"
        self.client_example["size"] = 150
        self.client_example["industry"] = "IT Services"
        self.client_example["email"] = "it.worx@example.com"
        crud_result = crud.update_client(self.db, self.client_id, self.client_example)
        assert crud_result.matched_count > 0

    def test_5_client_list(self):
        self.client_id = crud.create_client(self.db, self.client_example)
        crud_result = crud.get_client_list(self.db, 
            company=self.client_example,
            size_lte=(self.client_example["size"] + 100),
            size_gte=self.client_example["size"],
            country=self.client_example["country"],
            state=self.client_example["state"],
            zipcode=self.client_example["zipcode"],
            industry=self.client_example["industry"],
            services=self.client_example["services"],
            email=self.client_example["email"],
            operator="$and",
            skip=0,
            limit=1)
        assert isinstance(crud_result, pymongo.cursor.Cursor)
        assert len(list(crud_result)) > 0

    def test_6_delete_client(self):
        client_id = crud.create_client(self.db, self.client_example)
        crud_result = crud.delete_client(self.db, client_id)
        assert crud_result.deleted_count > 0
