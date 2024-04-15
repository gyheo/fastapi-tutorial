from typing import List, Union

from fastapi import FastAPI, Header
from typing_extensions import Annotated

app = FastAPI()


@app.get("/items1/")
async def read_items1(user_agent: Annotated[Union[str, None], Header()] = None):
    return {"User-Agent": user_agent}


# Automatic Conversion
@app.get("/items2/")
async def read_items2(strange_header: Annotated[Union[str, None], Header(convert_underscores=False)] = None):
    return {"strange_header": strange_header}


@app.get("/items3/")
async def read_items3(x_token: Annotated[Union[List[str], None], Header()] = None):
    return {"X-Token values": x_token}
