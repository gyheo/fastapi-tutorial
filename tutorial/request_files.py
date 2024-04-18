from typing import List, Union

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from typing_extensions import Annotated

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


# File Parameters with `UploadFile`
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


# Optional File Upload
@app.post("/files-optional/")
async def create_file_optional(file: Annotated[Union[bytes, None], File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile-optional/")
async def create_upload_file_optional(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


# `UploadFile` with Additional Metadata
@app.post("/files-metadata/")
async def create_file_metadata(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}


@app.post("/uploadfile-metadata")
async def create_upload_file_metadata(file: Annotated[UploadFile, File(description="A file read as UploadFile"),]):
    return {"filename": file.filename}


# Multiple File Uploads with Additional Metadata
@app.post("/files-multiple/")
async def create_files_multiple(files: Annotated[List[bytes], File(description="Multiple files as bytes")]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles-multiple/")
async def create_files_multiple(files: Annotated[List[UploadFile], File(description="Multiple files as UploadFile")]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
        <body>
        <form action="/files-multiple/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        <form action="/uploadfiles-multiple/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        </body>
    """

    return HTMLResponse(content=content)
