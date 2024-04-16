from typing import Any, List, Union

from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    # tax: Union[float, None] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


class BaseUser(BaseModel):
    username: str
    password: str
    full_name: Union[str, None] = None


class UserIn(BaseUser):
    email: EmailStr


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


# @app.post("/items/")
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/name", response_model=Item, response_model_include={"name", "description"})
async def read_item(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]


# @app.get("/items/")
@app.get("/items/", response_model=List[Item])
async def read_items() -> Any:
    return [
        Item(name="APPLE iPhone", price=135.0),
        Item(name="SAMSUNG Galaxy Flip", price=180.0)
    ]


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.google.com")


@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Union[Response, dict]:
    if teleport:
        return RedirectResponse(url="https://www.google.com")
    return {"message": "Here's your interdimensional portal"}
