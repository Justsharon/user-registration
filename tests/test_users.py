import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

DATABASE_URL = "sqlite://"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_lookup_unregistered_user(client):
    response = client.post(
        "/users/lookup",
        json={"phone_number": "+254712345678"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "registered": False,
        "message": "User not found"
    }

def test_register_new_user(client):
    response = client.post(
        "/users/register",
        json={
            "phone_number": "+254722123456",
            "full_name": "Jane Doe",
            "email": "jane@example.com",
            "id_number": "98765432"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Registration successful"
    }

def test_register_duplicate_phone_number(client):
    user = {
        "phone_number": "+254722123456",
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "id_number": "98765432"
    }

    first_response = client.post("/users/register", json=user)
    second_response = client.post("/users/register", json=user)

    assert first_response.status_code == 200
    assert second_response.status_code == 409

def test_register_duplicate_id_number(client):
    first_user = {
        "phone_number": "+254722123456",
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "id_number": "98765432"
    }

    second_user = {
        "phone_number": "+254733123456",
        "full_name": "John Doe",
        "email": "john@example.com",
        "id_number": "98765432"
    }

    first_response = client.post("/users/register", json=first_user)
    second_response = client.post("/users/register", json=second_user)

    assert first_response.status_code == 200
    assert second_response.status_code == 409

def test_register_invalid_phone_number(client):
    user = {
        "phone_number": "0712345678",
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "id_number": "98765432"
    }

    response = client.post("/users/register", json=user)

    assert response.status_code == 422

def test_register_invalid_email(client):
    user = {
        "phone_number": "+254722123456",
        "full_name": "Jane Doe",
        "email": "not-an-email",
        "id_number": "98765432"
    }

    response = client.post("/users/register", json=user)

    assert response.status_code == 422

def test_registered_user_can_be_found(client):
    user = {
        "phone_number": "+254722123456",
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "id_number": "98765432"
    }

    registration_response = client.post(
        "/users/register",
        json=user
    )

    lookup_response = client.post(
        "/users/lookup",
        json={"phone_number": "+254722123456"}
    )

    assert registration_response.status_code == 200
    assert lookup_response.status_code == 200
    assert lookup_response.json() == {
        "registered": True,
        "message": "User found"
    }