from enum import Enum
from typing import Set, Union

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Tags(Enum):
    items = "items"
    users = "users"


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


# Response Status Code / Tags / Summary and Response, description
@app.post("/items/",
          response_model=Item,
          summary="Create an Item",
          status_code=status.HTTP_201_CREATED,
          # description="Create an item with all the information, name, description, price, tax and a set of unique tags",
          response_description="The created item",
          tags=["items"])
async def create_item(item: Item):
    """
       Create an item with all the information:

       - **name**: each item must have a name
       - **description**: a long description
       - **price**: required
       - **tax**: if the item doesn't have tax, you can omit this
       - **tags**: a set of unique tag strings for this item
       """
    return item


# Tags with enums
@app.get("/items-enums/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]


@app.get("/users-enums/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Heo GeonYeong"}]


# Deprecate a path operation
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
