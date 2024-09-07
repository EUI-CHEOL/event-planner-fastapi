from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union
from models.mongo_events import Event
from beanie import Document

class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = Field(default=None)

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "ironofchoi@gmail.com",
                "password": "password",
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

class TokenResponse(BaseModel):
    access_token: str = Union[str, None]
token_type: str = Union[str, None]