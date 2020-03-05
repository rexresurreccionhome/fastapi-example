from typing import Optional, List, Set, Dict

from fastapi import APIRouter, Depends, Query, Body, HTTPException
from pydantic import EmailStr
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from pymongo.mongo_client import MongoClient

from database.database import get_db
from .schemas import Staff, StaffBasicInfo, StaffFullInfo, ObjectIdStr
from .schema_examples import staff_example
from .enums import (
    Gender as GenderEnum,
    Employment as EmploymentEnum,
    PayType as PayTypeEnum,
)
from . import crud


router = APIRouter()

@router.get("/list",
    response_model=List[StaffBasicInfo],
    summary="Return list of staff",
    description="Path function will return list of Staff from the DB with basic info only",
)
async def get_staff_list(
    gender: Optional[GenderEnum] = None,
    country: Optional[str] = None,
    state: Optional[str] = None,
    zipcode: Optional[str] = None,
    profession: Optional[str] = None,
    skills: List[str] = Query([], title="skills", description="Combine with Profession, search for one or more skills"),
    email: Optional[EmailStr] = None,
    age_lte: int = 0,
    age_gte: int = 0,
    skip: int = 0,
    limit: int = 100,
    db: MongoClient = Depends(get_db),
):
    crud_result = crud.get_staff_list(db, gender=gender, age_lte=age_lte, age_gte=age_gte, country=country, state=state,
                                    zipcode=zipcode, profession=profession, skills=skills, email=email, skip=skip, limit=limit)
    return list(crud_result)

@router.get("/get/{staff_id}",
    response_model=StaffFullInfo,
    summary="Return Staff",
    description="Path function will return Staff from the DB with full info",
)
async def get_staff(staff_id: ObjectIdStr, db: MongoClient = Depends(get_db)):
    crud_result = crud.get_staff(db, staff_id)
    if not crud_result:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Staff Profile Not Found.")
    return crud_result

@router.post("/create",
    status_code=HTTP_201_CREATED,
    response_model=StaffFullInfo,
    summary="Create Staff Profile",
    description="Path function will create Staff and return from the DB with full info",
)
async def create_staff(staff: Staff = Body(..., example=staff_example), db: MongoClient = Depends(get_db)):
    staff_id = crud.create_staff(db, staff)
    if not staff_id:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Failed to create Staff Profile.")
    staff = crud.get_staff(db, staff_id)
    return staff

@router.put("/update/{staff_id}",
    status_code=HTTP_202_ACCEPTED,
    response_model=StaffFullInfo,
    summary="Update Staff Profile",
    description="Path function will update Staff and return from the DB with updated full info",
)
async def update_staff(staff_id: ObjectIdStr, staff: Staff = Body(..., example=staff_example), db: MongoClient = Depends(get_db)):
    crud_result = crud.update_staff(db, staff_id, staff)
    if crud_result.matched_count == 0:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Staff was not updated. Does the Staff ID exists?")
    staff = crud.get_staff(db, staff_id)
    return staff


@router.delete("/delete/{staff_id}",
    status_code=HTTP_204_NO_CONTENT,
    summary="Delete Staff Profile",
    description="Path function will delete Staff from the DB",
)
async def delete_staff(staff_id: ObjectIdStr, db: MongoClient = Depends(get_db)):
    crud_result = crud.delete_staff(db, staff_id)

