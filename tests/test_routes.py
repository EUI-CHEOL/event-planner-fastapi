import httpx
import pytest
from auth.jwt_handler import create_access_token
from models.mongo_events import Event

@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("testuser@gmail.com")

@pytest.fixture(scope="module")
async def mock_event() -> Event:
    new_event = Event(
        creator="testuser@gmail.com",
        title="FastAPI",
        image="https://",
        description="We will be",
        tags=["python","fastapi"],
        location="Google Meet"
    )
    await Event.insert_one(new_event)
    yield new_event

@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    response = await default_client.get("/event/")
    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)


# test는 왤케 에러가 생길까나...