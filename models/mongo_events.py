from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import JSON, SQLModel, Field, Column
from beanie import Document
# from beanie import PydanticObjectId

class Event(Document):
    # id: PydanticObjectId = Field(default=None, primary_key=True)
    creator: Optional[str] = None
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str

    class Config:
        arbitarary_type_allowed = True
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "I will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }
    
    class Settings:
        name = "events"

class EventUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    image: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)
    location: Optional[str] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FFASTAPI",
                "image": "http://local",
                "description": "We will be discussing the contens",
                "tags": ["asd", "asdg", "glk"],
                "location": "Seoul"
            }
        }