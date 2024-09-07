import asyncio
import httpx
import pytest

from main import app
from database.mongo_connection import Settings
from models.mongo_events import Event
from models.mongo_users import User


@pytest.fixture(scope="session")
def event_loop():
    # policy = asyncio.get_event_loop_policy()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

async def init_db():
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb://localhost:27017/testdb"

    await test_settings.initialize_database()

@pytest.fixture(scope="session")
async def default_client():
    await init_db()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://app") as client:
        yield client
        await Event.find_all().delete()
        await User.find_all().delete()