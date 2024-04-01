from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = "sqlite:///./BookStoreTest.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user1(client):
    user_data = {"email": "abdo1@gmail.com",
                 "username" : "abdo1", 
                 "password": "password123"}
    res = client.post("/users/signUp", json=user_data)
    assert res.status_code == 201, "Response status code was not 201"
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "abdo2@gmail.com",
                 "username" : "abdo2", 
                 "password": "password123"}
    res = client.post("/users/signUp", json=user_data)
    assert res.status_code == 201, "Response status code was not 201"
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user1):
    return create_access_token({"user_id": test_user1['id']})

@pytest.fixture
def token2(test_user2):
    return create_access_token({"user_id": test_user2['id']})


@pytest.fixture
def authorized_client1(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def authorized_client2(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_book_categories(session):
    book_categories_data = [
        {
            "description" : "Drama"
        }, 
        {
            "description" : "Fantazy"
        }
    ]
    
    book_categories_to_create =  list(map(lambda bc : models.BookCategory(**bc), book_categories_data))
    session.add_all(book_categories_to_create)
    session.commit()
    return session.query(models.BookCategory).all()


@pytest.fixture
def test_books(test_user1, test_user2, session, test_book_categories):
    books_data = [
        {
            "title":  "test book 1", 
            "brief" : "brief about book 1", 
            "owner_id" : test_user1["id"], 
            "category_id" : test_book_categories[0].id
        }, 
        {
            "title":  "test book 2", 
            "brief" : "brief about book 2", 
            "owner_id" : test_user2["id"], 
            "category_id" : test_book_categories[1].id
        }
    ]
    
    book_to_create = list(map(lambda b : models.Book(**b), books_data))
    session.add_all(book_to_create)
    session.commit()
    return session.query(models.Book).all()