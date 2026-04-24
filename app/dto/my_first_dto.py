from typing import Literal, Self

from pydantic import BaseModel, Field, field_validator, model_validator

class SubModel(BaseModel):
    
    user_name: str = Field(description="Username from db")
    user_id: int = Field(description="User ID from db", ge=0)
    
    @field_validator("user_name", mode="after")
    @classmethod
    def validate_username(cls, value: str):
        if "_" in value:
            raise ValueError("No _ symbols allowed in username")
        return value
        
    @model_validator(mode="after")
    def validate_user_name_id(self) -> Self:
        
        if self.user_name == str(self.user_id):
            raise ValueError("Username can't be equal to user_id")
        return self

class MyFirstDto(BaseModel):
    
    first_field: str | None = Field(description="Field for first argument", default=None, examples=["field_one"])
    second_field: int = Field(ge=1, description="Int parameter", default=2, examples=[1, 2, 3])
    literal_field: Literal["one", "two"] = Field(examples=["one"])
    bool_field: bool = Field(description="bool_field")
    user_info: SubModel
    
class SecondDto(MyFirstDto):
    
    scenario_info: str = Field(description="Scenario description", default="Scenario description")
    