from fastapi import FastAPI, Request, Form, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
import fastapi.responses
from uvicorn import run
import os
import json
# Import custom modules
import serverInfoWrite

# check about middleware for blocking no logged users

# Get program dir for file usage
program_dir = os.path.dirname(os.path.abspath(__file__))
pages_dir = os.path.join(program_dir, "pages")

# templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))

json_path = os.path.join(program_dir, '..', 'server_properties.json')

# Create the FastAPI instance
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Redirect to /pages/menu.html
    return RedirectResponse(url='/pages/main.html')


@app.post("/submit-settings")
async def root(request: Request):
    form_data = await request.json()
    serverInfoWrite.set_settings_json_argument(form_data)


@app.post('/submit-rules')
async def root(request: Request):
    form_data = await request.json()
    serverInfoWrite.set_rules_json_argument(form_data)


@app.get("/check-switches")
async def check_switches():
    try:
        # Load current rules from server.json
        with open(json_path, 'r') as f:
            existing_data = json.load(f)
            rules = existing_data['rules']

        # Redirect with rules data as query parameter
        rules_string = json.dumps(rules)
        # url = "/pages/rules.html?rules=" + rules_string
        return JSONResponse(content=rules)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error fetching switch states: {e}")


@app.get("/check-settings")
async def check_settings():
    try:
        with open(json_path, 'r') as f:
            existing_data = json.load(f)

        del existing_data["rules"]
        return JSONResponse(content=existing_data, status_code=302)

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
app.mount("/pages", StaticFiles(directory=pages_dir), name="pages")

#main function
if __name__ == '__main__':
    run(app, port=20343)

