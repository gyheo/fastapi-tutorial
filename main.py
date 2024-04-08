from typing import List, Union

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing_extensions import Annotated

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# Create your data model
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}


# Query Parameter type conversion
# @app.get("/items/{item_id}")
# def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
#     item = {"item_id": item_id}
#
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item tha has a long description"}
        )
    return item


# Required query parameters
# @app.get("/items/{item_id}")
# def read_item(item_id: str, needy: str):
#     item = {"item_id": item_id, "needy": needy}
#     return item

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]

@app.get("/items/")
async def read_items(q: Annotated[Union[str, None], Query(title="Query String",
                                                          description="Query string for the items to search in the database that have a good match.",
                                                          min_length=3,
                                                          deprecated=True,
                                                          alias="item-query")] = None,
                                                          ):
    results ={"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.post("/items/")
# Declare it as a parameter
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
        # item_dict["price_with_tax"] = price_with_tax
    return item_dict


# Request body + path parameters
@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

