from fastapi import FastAPI, Request, Form, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from typing import Annotated
import fastapi.responses
from uvicorn import run
import os
# Import custom modules
import serverInfoWrite

# check about middleware for blocking no logged users

# Get program dir for file usage
program_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")

# templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))


# Create the FastAPI instance
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Use RedirectResponse to automatically redirect to /pages/menu.html
    return RedirectResponse(url="/pages/menu.html", status_code=200)


@app.post("/submit-settings")
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

# Serve static files from the "pages" directory
app.mount("/pages", StaticFiles(directory=program_dir), name="pages")

if __name__ == '__main__':
    run(app, port=20343)
