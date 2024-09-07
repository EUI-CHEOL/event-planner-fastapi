import pytest
from models.mongo_events import EventUpdate

@pytest.fixture
def event() -> EventUpdate:
    return EventUpdate(
        title="FASTAPIBOOK",
        image="https://fastapi.png",
        description="THIS IS SAMPLE",
        tags=["PYTHON","FASTAPI"],
        location="SEOUL"
    )

def test_event_name(event: EventUpdate) -> None:
    assert event.title == "FASTAPIBOOK"

def add(a: int, b: int) -> int:
    return a + b

def subtract(a: int, b:int) -> int:
    return b - a

def multiply(a: int, b:int) -> int:
    return a * b

def divide(a: int, b: int) -> int:
    return b // a

def test_add() -> None:
    assert add(1, 1) == 2, "틀렸는데"

def test_subtract() -> None:
    assert subtract(2, 5) == 3

def test_multiply() -> None:
    assert multiply(10, 10) == 100

def test_divide() -> None:
    assert divide(25, 100) == 4