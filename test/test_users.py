import pytest
from app import sechemaes, models
from app.config import settings
from jose import jwt


import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def test_create_user(client):
    res = client.post(
        "/users/signUp",
        json= {"email": "hello123@gmail.com"
              , "username": "hello123"
              , "password": "password123"})

    new_user = res.json()
    logging.warning(new_user)
    
    assert res.status_code == 201, "Response status code was not 201 (Created)"
    assert new_user["email"] == "hello123@gmail.com", "Email address is not as expected"
    assert new_user["username"] == "hello123", "Username is not as expected"
        


def test_create_multiple_users_with_the_same_details(client):
    res = client.post(
        "/users/signUp",
        json={"email": "hello123@gmail.com"
              , "username": "hello123"
              , "password": "password123"})

    new_user = res.json()
    assert new_user["email"] == "hello123@gmail.com", "Email address is not as expected"
    assert new_user["username"] == "hello123", "Username is not as expected"
    assert res.status_code == 201, "Response status code was not 201 (Created)"
    
    res = client.post(
        "/users/signUp",
        json={"email": "hello123@gmail.com"
              , "username": "hello122"
              , "password": "password123"})
    assert res.status_code == 400, "Response status code was not 400"
    assert res.json()["detail"] == "User with provided details already exists", "detail have wrong message returned"



def test_login_with_email(client, test_user1):
    res = client.post(
        "/users/login",
        data = {"username" :  test_user1["email"], "password" : test_user1["password"]}
    )
    
    assert res.status_code == 200, "Response status code was not 200"
    
    login_res =  sechemaes.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user1["id"], "User ID in the payload doesn't match expected"
    assert login_res.token_type == "bearer", "Token type is not 'bearer'"
    


def test_login_with_username(client, test_user1):
    res = client.post(
        "/users/login",
        data = {"username" :  test_user1["username"], "password" : test_user1["password"]}
    )
    
    assert res.status_code == 200, "Response status code was not 200"
    
    login_res =  sechemaes.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user1["id"], "User ID in the payload doesn't match expected"
    assert login_res.token_type == "bearer", "Token type is not 'bearer'"
    
@pytest.mark.parametrize("email, password, status_code", [
    ('abdo1@gmail.com', 'password123', 200),
    ('abdo1@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('abdo1@gmail.com', None, 422)
])
def test_incorrect_login(test_user1, client, email, password, status_code):
    res = client.post(
        "/users/login", data={"username": email, "password": password})

    assert res.status_code == status_code