from typing import Optional, List, Set, Dict

from fastapi import APIRouter, Depends, Query, Body, HTTPException
from pydantic import EmailStr
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from pymongo.mongo_client import MongoClient

from database.database import get_db
from .schemas import Client, ClientBasicInfo, ClientFullInfo
from staff.schemas import StaffHired, ObjectIdStr
from .schema_examples import client_example
from staff.schema_examples import staff_hired_example
from . import crud


router = APIRouter()

@router.get("/list",
    response_model=List[ClientBasicInfo],
    summary="Return list of client",
    description="Path function will return list of Client from the DB with basic info only",
)
async def get_client_list(
    company: Optional[str] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    zipcode: Optional[str] = None,
    industry: Optional[str] = None,
    services: List[str] = Query([], title="services", description="Combine with Industry, search for one or more services"),
    email: Optional[EmailStr] = None,
    size_lte: int = 0,
    size_gte: int = 0,
    skip: int = 0,
    limit: int = 100,
    db: MongoClient = Depends(get_db),
):
    crud_result = crud.get_client_list(db, company=company, size_lte=size_lte, size_gte=size_gte, country=country, state=state,
                                    zipcode=zipcode, industry=industry, services=services, email=email, skip=skip, limit=limit)
    return list(crud_result)

@router.post("/create",
    status_code=HTTP_201_CREATED,
    response_model=ClientFullInfo,
    summary="Create Client Profile",
    description="Path function will create Client and return from the DB with full info",
)
async def create_client(client: Client = Body(..., example=client_example), db: MongoClient = Depends(get_db)):
    client_id = crud.create_client(db, client)
    if not client_id:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Failed to create Client Profile.")
    client = crud.get_client(db, client_id)
    return client

@router.put("/update/{client_id}",
    status_code=HTTP_202_ACCEPTED,
    response_model=ClientFullInfo,
    summary="Update Client Profile",
    description="Path function will update Client and return from the DB with updated full info",
)
async def update_client(
    client_id: ObjectIdStr,
    client: Client = Body(..., example=client_example),
    staff_hired: List[StaffHired] = Body([], example=staff_hired_example, description="Explicitly update Staff Hired by the Company"),
    db: MongoClient = Depends(get_db)
):
    crud_result = crud.update_client(db, client_id, client, staff_hired=staff_hired)
    if crud_result.matched_count == 0:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Client was not updated. Does the Client ID exists?")
    if staff_hired:
        crud.update_staff_hired(db, client_id, staff_hired)
    client = crud.get_client(db, client_id)
    return client

@router.put("/update/staff_hired/{client_id}",
    status_code=HTTP_202_ACCEPTED,
    response_model=List[StaffHired],
    summary="Update Staff Hired",
    description="Path function will update Staff Hired in Client document and return from the DB with full list",
)
async def update_staff_hired(
    client_id: ObjectIdStr,
    staff_hired: List[StaffHired] = Body(..., example=staff_hired_example, description="Explicitly update Staff Hired by the Company"),
    db: MongoClient = Depends(get_db)
):
    crud_result = crud.update_staff_hired(db, client_id, staff_hired)
    if updated.matched_count == 0:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Staff Hired was not updated.")
    client = crud.get_client(db, client_id)
    return client["staff_hired"]

@router.delete("/delete/{client_id}",
    status_code=HTTP_204_NO_CONTENT,
    summary="Delete Client Profile",
    description="Path function will delete Client from the DB",
)
async def delete_client(client_id: ObjectIdStr, db: MongoClient = Depends(get_db)):
    crud_result = crud.delete_client(db, client_id)

