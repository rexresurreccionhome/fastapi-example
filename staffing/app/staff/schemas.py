from typing import Optional, List, Set, Dict
from datetime import datetime, date
from bson.objectid import ObjectId

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from pydantic.dataclasses import dataclass

from .enums import (
    Gender as GenderEnum,
    Employment as EmploymentEnum,
    PayType as PayTypeEnum,
)

from database.common import CommonConfig, ObjectIdStr


class StaffRole(BaseModel):
    title: str = Field(..., title="Job Title")
    department: str = Field(..., title="Department")
    employment: EmploymentEnum = Field(..., title="Employment")

class SalaryHistory(BaseModel):
    pay_rate: float = Field('0.00', title="Pay Rate")
    pay_type: PayTypeEnum = Field('Salary', title="Pay Type")
    pay_change: str = Field(None, title="Pay Change", description="Reason for any change in salary")
    period: str = Field('Biweekly', title="Pay Period")
    effective_date: date = Field(..., title="Effective Date")
 
class Staff(BaseModel):
    name: str = Field(..., title="Full Name")
    age: int = Field(..., title="Age", ge=0)
    gender: GenderEnum = Field(..., title="Gender")
    profession: str = Field(..., title="Occupation", description="e.g. Nurse, Engineer, IT, Manager")
    skills: Set[str] = Field([], title="Skills", description="Skill set related to the profession")
    email: EmailStr = Field(..., title="Email Address") 
    phone: str = Field(..., title="Phone")
    address: str = Field(..., title="Address")
    city: str = Field(..., title="City")
    state: str = Field(None, title="State")
    zipcode: str = Field(..., title="Zip Code")
    country: str = Field(..., title="Country Code")

class StaffBasicInfo(BaseModel):
    staff_id: ObjectIdStr = Field(..., alias="_id")
    name: str
    profession: str

    class Config(CommonConfig): pass

class StaffFullInfo(Staff):
    staff_id: ObjectIdStr = Field(..., alias="_id")

    class Config(CommonConfig): pass

class StaffHired(BaseModel):
    staff_id: ObjectIdStr = Field(..., alias="_id")
    role: StaffRole = Field(..., title="Job Role", description="Job role/position in the Company")
    salary: List[SalaryHistory] = Field([], title="Salary")
    hiredate: date = Field(..., title="Hire Date") 
    enddate: date = Field(None, title="End Date")
    active: bool = Field(True, title="Active", description="Status of employment")

    class Config(CommonConfig): pass


