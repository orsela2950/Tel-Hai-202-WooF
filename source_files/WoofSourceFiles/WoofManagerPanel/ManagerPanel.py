from fastapi import FastAPI, Response, Request, Form
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import fastapi.responses
from uvicorn import run
import os
# Import custom modules
import serverInfoWrite

# check about middleware for blocking no logged users

# Get program dir for file usage
program_dir = os.path.dirname(os.path.abspath(__file__))
# Create the FastAPI instance
app = FastAPI()


@app.get("/")
async def root(request: Request):
    # Add a page list in the main page
    return Response(content='<h1>Welcome to the woof manager panel!</h1>', status_code=200)


@app.post('/submit-settings')
async def root(request: Request, hostname: Annotated[str, Form()] = None,
               ip: Annotated[str, Form()] = None, port: Annotated[int, Form()] = None):
    
    new_settings = dict()

    if hostname:
        new_settings['host_name'] = hostname
    if ip:
        new_settings['ip'] = ip
    if port:
        new_settings['port'] = port

    serverInfoWrite.set_json_argument(new_settings)
    print(new_settings)
    # Return a redirect to home page or somthing
    return 'submitted'


@app.post('/submit-rules')
async def root(request: Request):
    form_data = await request.form()
    ddos_enabled = form_data.get("DDOS") == "on"  # True if enabled, False otherwise
    host_header_injection_enabled = form_data.get("HostHeaderInjection") == "on"
    # Access other options similarly
    return "ok ok"


@app.get("/favicon.ico")
async def root():
    favicon_path = os.path.join(program_dir, "favicon.ico")
    if os.path.isfile(favicon_path):
        return fastapi.responses.FileResponse(favicon_path)
    print("[!] cant find favicon")
    return None

app.mount("/", StaticFiles(directory=os.path.join(program_dir, "pages")), name="pages")

if __name__ == '__main__':
    run(app, port=20343)
