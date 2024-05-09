from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Use `StaticFiles`
# http://localhost:8000/static/logo-fastapi.png
app.mount("/static", StaticFiles(directory="static"), name="static")
