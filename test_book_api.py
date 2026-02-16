import pytest
from book_api import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_books_empty(client):
    response = client.get("/book_list")
    assert response.status_code == 200
    assert response.get_json() == []

def test_add_book(client):
    new_book = {"name": "The Great Gatsby", "price": 12.99}
    response = client.post("/book_list", json=new_book)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == new_book["name"]
    assert data["price"] == new_book["price"]
    assert "id" in data

def test_book_list_after_adding(client):
    response = client.get("/book_list")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1