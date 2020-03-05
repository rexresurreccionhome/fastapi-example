from datetime import datetime, timedelta

from .enums import Employment, PayType

now = datetime.now()
datetime(now.year, now.month + 6, now.day, 0, 0, 0).strftime("%Y/%m/%d")

staff_role_example = {
    "title": "Software Developer",
    "department": "Development",
    "employment": Employment.fulltime,
}

salary_history_example = {
    "pay_rate": float("80000"),
    "pay_type": PayType.salary,
    "pay_change": "Starting Salary",
    "period": "Biweekly",
    "effective_date": datetime.now().strftime('%Y-%m-%d'),
}

staff_example = {
    "name": "John Doe",
    "age": 31,
    "gender": "Male",
    "profession": "IT",
    "skills": [
        "Python",
        "Database Design",
    ],
    "email": "john.doe@example.com",
    "phone": "123-456-7890",
    "address": "Fake address somewhere",
    "city": "Chicago",
    "state": "IL",
    "zipcode": "60605",
    "country": "US",
}

staff_hired_example = [
    {
        "_id": "5e52e7e4fdf7de289a64d3d6",
        "role": {
            "title": "Software Developer",
            "department": "Development",
            "employment": Employment.fulltime,
        },
        "salary": [
            {
                "pay_rate": "80000",
                "pay_type": PayType.salary,
                "period": "Biweekly",
                "effective_date": datetime.now().strftime('%Y-%m-%d'),
            }
        ],
        "hiredate": now.strftime('%Y-%m-%d'),
        "active": 1,
    },
    {
        "_id": "5e52e36e4720d6b29afe7a00",
        "role": {
            "title": "Network Engineer",
            "department": "Network and Security",
            "employment": Employment.contract,
        },
        "salary": [
            {
                "pay_rate": "90000",
                "pay_type": PayType.hourly,
                "period": "Weekly",
                "effective_date": now.strftime('%Y-%m-%d'),
            }
        ],
        "hiredate": now.strftime('%Y-%m-%d'),
        "enddate": datetime(now.year, now.month + 6, now.day, 0, 0, 0).strftime("%Y-%m-%d"),
        "active": 1,
    },
]


