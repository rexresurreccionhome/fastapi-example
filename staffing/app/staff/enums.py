from enum import Enum


class Gender(str, Enum):
    male = "Male"
    female = "Female"

class Employment(str, Enum):
    fulltime = "Full-Time"
    parttime = "Part-Time"
    contract = "Contract"

class PayType(str, Enum):
    salary = "Salary"
    hourly = "Hourly"

