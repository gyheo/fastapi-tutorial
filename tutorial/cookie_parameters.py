from typing import Union

from fastapi import Cookie, FastAPI
from typing_extensions import Annotated

app = FastAPI()


# Declare `Cookie` Parameters
@app.get("/items/")
async def read_items(ads_id: Annotated[Union[str, None], Cookie()] = None):
    return {"ads_id": ads_id}
