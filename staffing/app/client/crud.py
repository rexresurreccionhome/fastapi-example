from typing import Optional, List, Set, Dict
from itertools import chain

from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId

from .schemas import Client
from staff.schemas import StaffHired
from database.common import ObjectIdStr

#default collection
def collection(db: MongoClient):
    db_staffing = db.staffing
    col_clients = db_staffing.clients
    return col_clients


#cruds

def get_client_list(
    db: MongoClient,
    company: str = None,
    size_lte: int = 0,
    size_gte: int = 0,
    country: str = None,
    state: str = None,
    zipcode: str = None,
    industry: str = None,
    services: List[str] = [],
    email: EmailStr = None,
    operator: str = None,
    skip: int = 0,
    limit: int = 100,
):
    filters = []
    if company:
        filters.append({"company": {"$regex": f"{company}", "$options": "$i"}})
    if size_lte:
        filters.append({"size": {"$lte": size_lte}})
    if size_gte:
        filters.append({"size": {"$gte": size_gte}})
    if country:
        filters.append({"country": country})
    if state:
        filters.append({"state": state})
    if zipcode:
        filters.append({"zipcode": zipcode})
    if industry:
        filters.append({"industry": {"$regex": f"{industry}", "$options": "$i"}})
    if services:
        filters.append({"services": {"$in": services}})
    if email:
        filters.append({"email": email})
    if len(filters):
        logical_operator = {(operator or "$and"): filters}
    else:
        logical_operator = {}
    client_list = collection(db)\
                .find(logical_operator)\
                .skip(skip)\
                .limit(limit)
    return client_list

def get_client(db: MongoClient, client_id: ObjectIdStr):
    document = collection(db).find_one({"_id": ObjectId(client_id)})
    return document

def update_client(db: MongoClient, client_id: ObjectIdStr, client: Client, staff_hired: List[StaffHired] = None):
    updated = collection(db).update_one({"_id": ObjectId(client_id)}, {"$set": jsonable_encoder(client)})
    return updated

def create_client(db: MongoClient, client: Client):
    client_id = collection(db).insert_one(jsonable_encoder(client)).inserted_id
    return client_id

def update_staff_hired(db: MongoClient, client_id: ObjectIdStr, staff_hired: List[StaffHired]):
    client = get_client(db, client_id)
    if not client:
        return
    if not client.get("staff_hired"):
        client["staff_hired"] = jsonable_encoder(staff_hired)
    else:
        updated_hired = []
        for i, s in enumerate(staff_hired):
            #print(s.dict(by_alias=True))
            sd = jsonable_encoder(s)
            for x, z in enumerate(client["staff_hired"]):
                if sd["_id"] == z["_id"] and z["active"]:
                    client["staff_hired"][x].update(sd)
                    updated_hired.append(s.staff_id)
        staff_hired = [s for s in staff_hired if s.staff_id not in updated_hired]
        if staff_hired:
            client["staff_hired"] = list(chain(client["staff_hired"], jsonable_encoder(staff_hired)))
    updated = collection(db).update_one({"_id": client["_id"]}, {"$set": {"staff_hired": client["staff_hired"]}})
    return updated

def delete_client(db: MongoClient, client_id: ObjectIdStr):
    deleted = collection(db).delete_one({"_id": ObjectId(client_id)})
    return deleted

