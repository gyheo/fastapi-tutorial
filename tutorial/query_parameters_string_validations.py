from typing import Union

from fastapi import FastAPI, Query
from typing_extensions import Annotated

app = FastAPI()


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
