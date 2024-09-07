from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from models.events import Event

class User(BaseModel):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "ironofchoi@gmail.com",
                "username": "euicheol",
                "events": [],
            }
        }

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "ironofchoi@gmail.com",
                "password": "asdf1234",
                "events": [],
            }
        }