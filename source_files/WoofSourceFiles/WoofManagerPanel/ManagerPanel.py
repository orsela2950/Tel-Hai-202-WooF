import fastapi
import uvicorn
from uvicorn import run
import os
app = fastapi.FastAPI()

async def get_favicon_path():
    """Returns the full path to the favicon ICO file placed near the program."""

    program_path = os.path.abspath(__file__)
    program_dir = os.path.dirname(program_path)
    favicon_path = os.path.join(program_dir, "favicon.ico")
    return favicon_path

@app.get("/")
async def root(request: fastapi.Request):
    return fastapi.Response(content='<h1>Welcome to the woof manager panel!</h1>', status_code=200)

@app.get("/favicon.ico")
async def root():
    favicon_path = await get_favicon_path()
    if os.path.isfile(favicon_path):
        return fastapi.responses.FileResponse(favicon_path)
    print("[!] cant find favicon")
    return None


if __name__ == '__main__':
    uvicorn.run(app, port=20343)
