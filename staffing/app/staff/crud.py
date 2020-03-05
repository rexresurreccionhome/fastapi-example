from typing import Optional, List, Set, Dict

from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId

from .enums import (
    Gender as GenderEnum,
    Employment as EmploymentEnum,
    PayType as PayTypeEnum,
)
from .schemas import Staff, ObjectIdStr

#default collection
def collection(db: MongoClient):
    db_staffing = db.staffing
    col_staff = db_staffing.staff
    return col_staff

#cruds

def get_staff_list(
    db: MongoClient,
    gender: GenderEnum = None,
    age_lte: int = 0,
    age_gte: int = 0,
    country: str = None,
    state: str = None,
    zipcode: str = None,
    profession: str = None,
    skills: List[str] = [],
    email: EmailStr = None,
    operator: str = None,
    skip: int = 0,
    limit: int = 100
):
    filters = []
    if gender:
        filters.append({"gender": gender})
    if age_lte:
        filters.append({"age": {"$lte": age_lte}})
    if age_gte:
        filters.append({"age": {"$gte": age_gte}})
    if country:
        filters.append({"country": country})
    if state:
        filters.append({"state": state})
    if zipcode:
        filters.append({"zipcode": zipcode})
    if profession:
        filters.append({"profession": {"$regex": f"{profession}", "$options": "$i"}})
    if skills:
        filters.append({"skills": {"$in": skills}})
    if email:
        filters.append({"email": email})
    if len(filters):
        logical_operator = {(operator or "$and"): filters}
    else:
        logical_operator = {}
    staff_list = collection(db)\
                .find(logical_operator)\
                .skip(skip)\
                .limit(limit)
    return staff_list

def get_staff(db: MongoClient, staff_id: ObjectIdStr):
    document = collection(db).find_one({"_id": ObjectId(staff_id)})
    return document

def update_staff(db: MongoClient, staff_id: ObjectIdStr, staff: Staff):
    updated = collection(db).update_one({"_id": ObjectId(staff_id)}, {"$set": jsonable_encoder(staff)})
    return updated

def create_staff(db: MongoClient, staff: Staff):
    staff_id = collection(db).insert_one(jsonable_encoder(staff)).inserted_id
    return staff_id

def delete_staff(db: MongoClient, staff_id: ObjectIdStr):
    deleted = collection(db).delete_one({"_id": ObjectId(staff_id)})
    return deleted

