from fastapi import APIRouter, HTTPException, status, Depends
# from models.events import Event, EventUpdate
from models.mongo_events import Event, EventUpdate
from typing import List, Union
# from sqlmodel import select
from beanie import PydanticObjectId
from database.mongo_connection import Database
from auth.authenticate import authenticate

event_router = APIRouter(
    tags=["Events"]
)


event_database = Database(Event)

@event_router.get("/", response_model=Union[List[Event], List])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    if not events:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="찾으시는 이벤트가 없습니다."
        )
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if event:
        return event
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

@event_router.post("/new")
async def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    body.creator = user
    await event_database.save(body)

    return {
        "message": "Event created successfully."
    }

@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate, user: str = Depends(authenticate)) -> Event:
    event = await event_database.get(id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed"
        )
    updated_event = await event_database.update(id, body)
    if not update_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_event

@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await event_database.get(id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operation not allowed. 권한이 없습니다."
        )

    events = await event_database.delete(id)
    if not events:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )

    return {
        "message": "Event deleted successfully."
    }

# @event_router.delete("/")
# async def delete_all_events() -> dict:
#     events.clear()
#     return {
#         "message": "Events deleted succesfully."
#     }

# @event_router.put("/edit/{id}", response_model=Event)
# async def update_event(id: int, new_data: EventUpdate, session=Depends(get_session)) -> Event:
#     event = session.get(Event, id)
#     if event:
#         event_data = new_data.model_dump(exclude_unset=True)
#         for key, value in event_data.items():
#             setattr(event, key, value)
#         session.add(event)
#         session.commit()
#         session.refresh(event)

#         return event
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Event with supplied ID does not exist"
#     )

# @event_router.delete("/delete/{id}")
# async def delete_event(id: int, session=Depends(get_session)) -> dict:
#     event = session.get(Event, id)
#     if event:
#         session.delete(event)
#         session.commit()
#         return {
#             "message": "Event deleted successfully"
#         }

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Event with supplied ID does not exist."
#     )