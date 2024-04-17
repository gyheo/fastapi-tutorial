from fastapi import FastAPI, status

app = FastAPI()


# Shortcut to remember the names
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
