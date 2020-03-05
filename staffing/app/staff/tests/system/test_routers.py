from fastapi import FastAPI
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from starlette.testclient import TestClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from database.database import get_db
from staff import crud
from staff.schemas import StaffFullInfo
from staff.schema_examples import staff_example
from staff.enums import  Gender as GenderEnum
from main import app

from urllib.parse import urlencode
import pymongo
import pydantic
import pytest


class TestRouter:

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

    def setup_method(self, method):
        self.staff_id = None
        self.staff_example = staff_example.copy()

    def teardown_method(self, method):
        if self.staff_id:
            self.client.delete(f"/staff/delete/{self.staff_id}", headers={})

    def test_1_create_staff(self):
        response = self.client.post("/staff/create", headers={}, json=self.staff_example)
        assert response.status_code == HTTP_201_CREATED
        staff = response.json()
        assert isinstance(staff, dict)
        assert "_id" in staff
        self.staff_id = staff["_id"]
        staff_model = StaffFullInfo(**staff)
        assert staff_model.staff_id == ObjectId(self.staff_id)
        with pytest.raises(pydantic.ValidationError):
            del staff["_id"]
            staff_model = StaffFullInfo(**staff)#test ValidationError

    def test_2_update_staff(self):
        response = self.client.post("/staff/create", headers={}, json=self.staff_example)
        assert response.status_code == HTTP_201_CREATED
        staff = response.json()
        self.staff_id = staff["_id"]
        self.staff_example["name"] = "Poison Ivy"
        self.staff_example["age"] = 29
        self.staff_example["gender"] = GenderEnum.female
        self.staff_example["profession"] = "IT Specialist"
        self.staff_example["email"] = "posion.ivy@example.com"
        response = self.client.put(f"/staff/update/{self.staff_id}", headers={}, json=self.staff_example)
        assert response.status_code == HTTP_202_ACCEPTED
        staff = response.json()
        assert staff["name"] == self.staff_example["name"]
        assert staff["age"] == self.staff_example["age"]
        assert staff["gender"] == self.staff_example["gender"]
        assert staff["profession"] == self.staff_example["profession"]
        assert staff["email"] == self.staff_example["email"]

    def test_3_get_staff(self):
        response = self.client.post("/staff/create", headers={}, json=self.staff_example)
        assert response.status_code == HTTP_201_CREATED
        staff = response.json()
        self.staff_id = staff["_id"]
        response = self.client.get(f"/staff/get/{self.staff_id}", headers={})
        assert response.status_code == HTTP_200_OK

    def test_4_staff_list(self):
        response = self.client.post("/staff/create", headers={}, json=self.staff_example)
        assert response.status_code == HTTP_201_CREATED
        staff = response.json()
        self.staff_id = staff["_id"]
        query = urlencode({
            "gender": staff["gender"],
            "age_lte": (self.staff_example["age"] + 10),
            "age_gte": staff["age"],
            "country": staff["country"],
            "state": staff["state"],
            "zipcode": staff["zipcode"],
            "skills": staff["skills"],
            "profession": staff["profession"],
            "email": staff["email"],
            "operator": "$and",
            "skip": 0,
            "limit": 1,
        }, doseq=True)
        response = self.client.get(f"/staff/list?{query}", headers={})
        assert response.status_code == HTTP_200_OK
        staff_list = response.json()
        assert isinstance(staff_list, list)
        assert len(staff_list) > 0

    def test_5_delete_staff(self, monkeypatch):
        response = self.client.post("/staff/create", headers={}, json=self.staff_example)
        assert response.status_code == HTTP_201_CREATED
        staff = response.json()
        response = self.client.delete("/staff/delete/{}".format(staff["_id"]), headers={})
        assert response.status_code == HTTP_204_NO_CONTENT
        response = self.client.get("/staff/get/{}".format(staff["_id"]), headers={})
        assert response.status_code == HTTP_404_NOT_FOUND
