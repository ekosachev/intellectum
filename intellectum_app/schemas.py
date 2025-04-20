from pydantic import BaseModel, Field

class Student(BaseModel):
    last_name: str = Field(serialization_alias="Фамилия")
    first_name: str = Field(serialization_alias="Имя")
    phone_number: str = Field(serialization_alias="Номер телефона")
