import pytest
from app import models, sechemaes, utils


def test_filtered_query_with_category_id(client, test_books, test_book_categories):
    res = client.get(
            "/books/list",
            params={"category_id": test_book_categories[0].id, "limit": 10, "skip": 0}
        )
    assert res.status_code == 200, "Response status code was not 200 (Ok)"
    books = res.json()
    for book in books:
            assert book.get("category_id") == test_book_categories[0].id, "There are books with different category id"
        


def test_filtered_query_with_owner_id(client, test_books, test_user1):
    res = client.get(
            "/books/list",
            params={"owners_ids": test_user1["id"], "limit": 10, "skip": 0}
        )
    assert res.status_code == 200, "Response status code was not 200 (Ok)"
    books = res.json()
    for book in books:
            assert book.get("owner_id") == test_user1["id"], "There are books with different owner id"
        


def test_create_book_with_authorized_client(authorized_client1, test_user1, test_book_categories):
    res = authorized_client1.post(
        "/books/new", 
        json= {
            "title" : "Test 1", 
            "brief" : "Test 1 brief",
            "category_id" : test_book_categories[0].id, 
            "created_at" : utils.get_current_datetime().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
    )
    new_book =  res.json()
    assert res.status_code == 201, "Response status code was not 201 (Created)"
    assert new_book["owner_id"] == test_user1["id"], "user logined isn't the one who created the book"
    
def test_create_book_without_authorized_client(client, test_user1, test_book_categories):
    res = client.post(
        "/books/new", 
        json= {
            "title" : "Test 1", 
            "brief" : "Test 1 brief",
            "category_id" : test_book_categories[0].id, 
            "created_at" : utils.get_current_datetime().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
    )
    new_book =  res.json()
    assert res.status_code == 401, "Response status code was not 401 (Unauthorized)"
    
def test_create_book_with_wrong_category_id(authorized_client1, test_book_categories):
    res = authorized_client1.post(
        "/books/new", 
        json= {
            "title" : "Test 1", 
            "brief" : "Test 1 brief",
            "category_id" : -1, 
            "created_at" : utils.get_current_datetime().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
    )
    new_book = res.json()
    assert res.status_code == 400, "Response status code was not 400 (BadRequest)"
    
    
def test_eidt_book_with_same_user(authorized_client1, test_books, test_book_categories):
    res = authorized_client1.put(
        "/books/edit", 
        json= {
            "id" : test_books[0].id, 
            "title" : "Test 1 After Update", 
            "brief" : "Test 1 brief After Update",
            "category_id" : test_book_categories[0].id, 
            "created_at" : utils.get_current_datetime().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
    )
    
    edit_book =  res.json()
    assert res.status_code == 200, "Response status code was not 200 (Ok)"
    assert edit_book.get("title") == "Test 1 After Update", "Title was not updated successfully"
    assert edit_book.get("brief") == "Test 1 brief After Update", "brief was not updated successfully"
    
    
def test_eidt_book_with_another_user(authorized_client2, test_books, test_book_categories):
    res = authorized_client2.put(
        "/books/edit", 
        json= {
            "id" : test_books[0].id, 
            "title" : "Test 1 After Update", 
            "brief" : "Test 1 brief After Update",
            "category_id" : test_book_categories[0].id, 
            "created_at" : utils.get_current_datetime().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
    )
    
    edit_book =  res.json()
    assert res.status_code == 403, "Response status code was not 403 (Ok)"