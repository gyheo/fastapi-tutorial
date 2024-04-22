from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel


# Install custom exception handler
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


class Item(BaseModel):
    title: str
    size: int


@app.post("/items/")
async def create_item(item: Item):
    return item


items = {"foo": "The Foo Wrestlers"}


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."}
    )


# Override the default exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# Re-use FastAPI's exception handlers
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP Error! : {repr(exc)}")
    return await http_exception_handler


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # return PlainTextResponse(str(exc), status_code=400)
    # return JSONResponse(
    #     status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #     content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    # )
    print(f"OMG! The client sent invalid data: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # if item_id not in items:
    #     raise HTTPException(status_code=404,
    #                         detail="Item not found",
    #                         headers={"X-Error": "There goes my error"})

    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! It doesn't permit 3")
    return {"item_id": item_id}
