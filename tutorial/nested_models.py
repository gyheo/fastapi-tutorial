from typing import Dict, List, Set, Union

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Union[str, None]
    price: float
    tax: Union[float, None] = None
    # tags: list = []
    # tags: List[str] = []    # "list of strings"
    tags: Set[str] = set()  # duplicate data, it will be converted to a set of unique items
    images: Union[List[Image], None] = None


# Deeply nested models
class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: List[Item]


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# Bodies of pure lists
@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images


# Bodies of arbitrary `dict`s
@app.post("/index-weights")
async def create_index_weights(weights: Dict[int, float]):
    return weights
