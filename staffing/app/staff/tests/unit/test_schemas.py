from datetime import datetime, date
from typing import Optional, List, Set, Dict
from bson.objectid import ObjectId
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from staff.schemas import (
    StaffRole,
    SalaryHistory,
    StaffBasicInfo,
    StaffFullInfo,
    StaffHired,
)
from staff.schema_examples import (
    staff_role_example,
    salary_history_example,
    staff_example,
    staff_hired_example,
)
from staff.enums import (
    Gender as GenderEnum,
    Employment as EmploymentEnum,
    PayType as PayTypeEnum,
)
import pydantic
import pytest

class TestSchema:

    @classmethod
    def setup_class(cls):
        cls.staff_id = ObjectId()

    @classmethod
    def teardown_class(cls):
        pass

    def test_staff_role(self):
        model = StaffRole(**staff_role_example)
        assert jsonable_encoder(model) == staff_role_example
        assert isinstance(model.title, str)
        assert isinstance(model.department, str)
        assert isinstance(model.employment, EmploymentEnum)
        assert model.employment == EmploymentEnum.fulltime

    def test_salary_history(self):
        model = SalaryHistory(**salary_history_example)
        assert jsonable_encoder(model) == salary_history_example
        assert isinstance(model.pay_rate, float)
        assert isinstance(model.pay_type, PayTypeEnum)
        assert isinstance(model.pay_change, str)
        assert isinstance(model.period, str)
        assert isinstance(model.effective_date, date)

    def test_staff_full_info(self):
        #StaffFullInfo inherits all the property of Staff class
        model = StaffFullInfo(staff_id=self.staff_id, **staff_example)
        assert model.staff_id == model.dict(by_alias=True)["_id"]
        assert isinstance(model.name, str)
        assert isinstance(model.age, int)
        assert isinstance(model.gender, GenderEnum)
        assert isinstance(model.skills, (List, Set))
        assert isinstance(model.email, (str, EmailStr))
        with pytest.raises(pydantic.ValidationError):
            model = StaffFullInfo(**staff_example)

    def test_staff_basic_info(self):
        model = StaffBasicInfo(staff_id=self.staff_id, **staff_example)
        assert model.staff_id == model.dict(by_alias=True)["_id"]
        assert isinstance(model.name, str)
        assert isinstance(model.profession, str)
        assert model.name == staff_example["name"]

    def test_staff_hired(self):
        model = StaffHired(staff_id=self.staff_id, **staff_hired_example[1])
        assert model.staff_id == model.dict(by_alias=True)["_id"]
        assert isinstance(model.role, StaffRole)
        assert isinstance(model.salary[0], SalaryHistory)
        assert isinstance(model.hiredate, date)
        assert isinstance(model.enddate, date)
