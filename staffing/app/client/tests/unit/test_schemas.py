from datetime import datetime, date
from typing import Optional, List, Set, Dict
from bson.objectid import ObjectId
from pydantic import EmailStr
from fastapi.encoders import jsonable_encoder
from client.schemas import (
    Client,
    ClientBasicInfo,
    ClientFullInfo,
)
from staff.schemas import (
    StaffRole,
    StaffHired,
    SalaryHistory,
)
from client.schema_examples import client_example
from staff.schema_examples import staff_hired_example
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
        cls.client_id = ObjectId()

    @classmethod
    def teardown_class(cls):
        pass

    def test_client(self):
        model = Client(**client_example)
        assert isinstance(model.company, str)
        assert isinstance(model.size, int)
        assert isinstance(model.industry, str)
        assert isinstance(model.services, Set)
        assert isinstance(model.email, str)
        assert isinstance(model.phone, str)
        assert isinstance(model.address, str)
        assert isinstance(model.city, str)
        assert isinstance(model.state, str)
        assert isinstance(model.zipcode, str)
        assert isinstance(model.country, str)
        with pytest.raises(pydantic.ValidationError):
            model = Client(company=client_example['company'], industry=client_example['industry'])

    def test_client_basic_info(self):
        model = ClientBasicInfo(client_id=self.client_id, company=client_example['company'], industry=client_example['industry'])
        assert model.client_id == model.dict(by_alias=True)["_id"]
        assert isinstance(model.company, str)
        assert isinstance(model.industry, str)

    def test_client_full_info(self):
        model = ClientFullInfo(client_id=self.client_id, staff_hired=staff_hired_example, **client_example)
        assert model.client_id == model.dict(by_alias=True)["_id"]
        assert isinstance(model.company, str)
        assert isinstance(model.size, int)
        assert isinstance(model.industry, str)
        assert isinstance(model.services, Set)
        assert isinstance(model.email, str)
        assert isinstance(model.phone, str)
        assert isinstance(model.address, str)
        assert isinstance(model.city, str)
        assert isinstance(model.state, str)
        assert isinstance(model.zipcode, str)
        assert isinstance(model.country, str)
        assert isinstance(model.staff_hired, list)
        assert isinstance(model.staff_hired[0], StaffHired)
        with pytest.raises(pydantic.ValidationError):
            model = ClientFullInfo(**client_example)
