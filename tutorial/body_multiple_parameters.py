from typing import Union

from fastapi import Body, FastAPI, Path
from pydantic import BaseModel
from typing_extensions import Annotated

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


# Mix Path, Query and body parameters
@app.put("/items/{item_id}")
async def update_item(
        item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
        q: Union[str, None] = None,
        item: Union[Item, None] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# Multiple body parameters
@app.put("/items_multi_body/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# Singular values in body
@app.put("/items_singular/{item_id}")
async def update_item(item_id: int,
                      item: Item,
                      user: User,
                      importance: Annotated[int, Body(gt=0)]):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# Embed a single body parameter
@app.put("/items_embed/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
