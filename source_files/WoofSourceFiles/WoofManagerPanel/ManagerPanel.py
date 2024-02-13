from fastapi import FastAPI, Request, Form, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from typing import Annotated
import fastapi.responses
from uvicorn import run
import os
import sys
from os import path
import json
# Import custom modules
import serverInfoWrite

# check about middleware for blocking no logged users

# Get program dir for file usage
program_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))

json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'server_properties.json')
# Create the FastAPI instance
app = FastAPI()


def update_server_rules_json(new_data):
    with open(json_path, 'r') as f:
        existing_data = json.load(f)

    # Update rules based on received data
    existing_data['rules'] = {
        key: new_data.get(key) == "on"  # Use `.get` to handle missing keys
        for key in existing_data['rules']
    }

    # Write updated data to the file
    with open(json_path, 'w') as f:
        json.dump(existing_data, f, indent=4)
    return existing_data


def update_server_setting_json(new_data):
    with open(json_path, 'r') as f:
        existing_data = json.load(f)

    for key in existing_data:
        if new_data.get(key):
            existing_data[key] = new_data.get(key)
    existing_data["port"] = int(existing_data["port"])
    # Write updated data to the file
    with open(json_path, 'w') as f:
        json.dump(existing_data, f, indent=4)
    return existing_data


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Use RedirectResponse to automatically redirect to /pages/menu.html
    return RedirectResponse(url="/pages/menu.html", status_code=302)


@app.post("/submit-settings")
async def root(request: Request):
    # Access form data and update server.json
    form_data = await request.form()
    with open(json_path, 'r') as f:
        existing_data = json.load(f)

    new_settings = {
        "server_host": existing_data["server_host"],
        "ip": existing_data["ip"],
        "port": existing_data["port"],
    }
    update_server_setting_json(form_data)

    # Redirect with settings data as query parameters
    settings_string = json.dumps(new_settings)
    url = f"/pages/settings.html?settings={settings_string}"
    return RedirectResponse(url=url, status_code=302)


@app.post('/submit-rules')
async def root(request: Request):
    # Access form data and update server.json
    form_data = await request.form()
    update_server_rules_json(form_data)

    # Load current rules from server.json
    with open(json_path, 'r') as f:
        existing_data = json.load(f)
        rules = existing_data['rules']

    # Redirect with rules data as query parameter
    rules_string = json.dumps(rules)
    url = "/pages/rules.html?rules=" + rules_string
    return RedirectResponse(url=url, status_code=302)


@app.get("/check-switches")
async def check_switches():
    try:
        # Load current rules from server.json
        with open(json_path, 'r') as f:
            existing_data = json.load(f)
            rules = existing_data['rules']

        # Redirect with rules data as query parameter
        rules_string = json.dumps(rules)
        url = "/pages/rules.html?rules=" + rules_string
        print(url)
        return JSONResponse(content={"url": url}, status_code=302)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error fetching switch states: {e}")


@app.get("/check-settings")
async def check_settings():
    try:
        with open(json_path, 'r') as f:
            existing_data = json.load(f)

        new_settings = {
            "server_host": existing_data["server_host"],
            "ip": existing_data["ip"],
            "port": existing_data["port"],
        }

        # Redirect with settings data as query parameters
        settings_string = json.dumps(new_settings)
        url = f"/pages/settings.html?settings={settings_string}"
        print(url)
        return JSONResponse(content={"url": url}, status_code=302)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error fetching switch states: {e}")


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
