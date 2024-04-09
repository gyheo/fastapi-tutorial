from typing import Union

from fastapi import FastAPI, Path, Query
from typing_extensions import Annotated

app = FastAPI()


# Number validations: floats, greater than and less than


@app.get("/items/{item_id}")
async def read_items(
        *, item_id: Annotated[int, Path(title="The Id of the item to get", ge=0, le=1000)],
        q: str,
        size: Annotated[float, Query(gt=0, lt=10.5)]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
        results.update({"size": size})

    return results

