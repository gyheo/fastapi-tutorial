from fastapi.testclient import TestClient

from main_extended import app

client = TestClient(app)

VALID_TOKEN = {"X-Token": "coneofsilence"}
INVALID_TOKEN_RESPONSE = {"detail": "Invalid X-Token header"}


# Extended testing file
def test_read_item():
    response = client.get("/items/foo", headers=VALID_TOKEN)
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero"
    }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers=VALID_TOKEN)
    assert response.status_code == 400
    assert response.json() == INVALID_TOKEN_RESPONSE


def test_read_item_nonexistent_token():
    response = client.get("/items/baz", headers=VALID_TOKEN)
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers=VALID_TOKEN,
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "fakeofsilence"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == INVALID_TOKEN_RESPONSE


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers=VALID_TOKEN,
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}
