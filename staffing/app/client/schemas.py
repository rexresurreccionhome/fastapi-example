from abc import ABC
from typing import Optional, List, Set, Dict
from datetime import datetime, date

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from database.common import CommonConfig, ObjectIdStr
from staff.schemas import StaffHired

class Client(BaseModel):
    company: str = Field(..., title="Full Name")
    size: int = Field(..., title="Company Size", ge=0)
    industry: str = Field(..., title="Industry", description="e.g. Information Technology, Health Care, Retail")
    services: Set[str] = Field([], title="Services")
    email: EmailStr = Field(..., title="Email Address") 
    phone: str = Field(..., title="Phone")
    address: str = Field(..., title="Address")
    city: str = Field(..., title="City")
    state: str = Field(None, title="State")
    zipcode: str = Field(..., title="Zip Code")
    country: str = Field(..., title="Country Code")

class ClientBasicInfo(BaseModel):
    client_id: ObjectIdStr = Field(..., alias="_id")
    company: str
    industry: str

    class Config(CommonConfig): pass

class ClientFullInfo(Client):
    client_id: ObjectIdStr = Field(..., alias="_id")
    staff_hired: List[StaffHired] = Field([], title="Staff Hired")

    class Config(CommonConfig): pass


