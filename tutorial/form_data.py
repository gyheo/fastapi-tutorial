from fastapi import FastAPI, Form
from typing_extensions import Annotated

app = FastAPI()


# Define `Form` parameters
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
