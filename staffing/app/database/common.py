from bson.objectid import ObjectId


class CommonConfig:
    arbitrary_types_allowed = True
    allow_population_by_field_name = True
    json_encoders = {ObjectId: lambda x: str(x)}

class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not  ObjectId.is_valid(str(v)):
            return ValueError("'{v}' is not a valid ObjectId")
        return ObjectId(str(v))

