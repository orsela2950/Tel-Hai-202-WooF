from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import uvicorn
import os
from urllib.parse import urlparse

app = FastAPI()


async def get_favicon_path():
    """Returns the full path to the favicon ICO file placed near the program."""

    program_path = os.path.abspath(__file__)
    program_dir = os.path.dirname(program_path)
    favicon_path = os.path.join(program_dir, "favicon.ico")
    return favicon_path


@app.get("/")
async def root(request: Request):
    return "GET requested host " + request.headers.get("Host")

@app.get("/favicon.ico")
async def root():
    favicon_path = await get_favicon_path()
    if os.path.isfile(favicon_path):
        return FileResponse(favicon_path)
    print("[!] cant find favicon")
    return None

@app.post("/")
async def root(request: Request):
    return "POST request |" + (await request.body()).decode()



print("-= ==WEBSERVER TESTER== =-")
# Run the FastAPI app using uvicorn and specify the host and port to listen on
uvicorn.run(app,port=8000)
