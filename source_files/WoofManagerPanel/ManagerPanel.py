from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from uvicorn import run
from os.path import join, abspath, dirname, isfile
import json
# Import custom modules
import serverInfoWrite

PORT = 20343
# Ip is the loopback ip localhost/127.0.0.1

# Get program dir and path for use
program_dir = abspath(dirname(__file__))
pages_dir = join(program_dir, 'pages')
json_path = join(program_dir, '..', 'WoofSourceFiles/server_properties.json')
logs_dir = join(program_dir, '..', 'logs')
logs_path = join(logs_dir, 'main.toml')
security_logs_path = join(logs_dir, 'security.toml')

# Create the FastAPI instance
app = FastAPI()


@app.get('/')
async def root():
    # Redirect to /pages/main.html
    return RedirectResponse(url='/pages/main.html')


@app.post('/submit-settings')
async def root(request: Request):
    form_data = await request.json()
    serverInfoWrite.set_settings_json_argument(form_data)


@app.post('/submit-rules')
async def root(request: Request):
    form_data = await request.json()
    serverInfoWrite.set_rules_json_argument(form_data)


@app.get('/check-switches')
async def root():
    try:
        # Load current rules from server.json
        with open(json_path, 'r') as f:
            existing_data = json.load(f)
            rules = existing_data['rules']

        return JSONResponse(content=rules)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error fetching switch states: {e}')


@app.get('/check-settings')
async def root():
    try:
        with open(json_path, 'r') as f:
            existing_data = json.load(f)

        del existing_data['rules']
        return JSONResponse(content=existing_data)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error fetching switch states: {e}')


@app.get('/logs')
async def root():
    return FileResponse(logs_path)


@app.get('/security_logs')
async def root():
    return FileResponse(security_logs_path)


@app.get('/favicon.ico')
async def root():
    favicon_path = join(program_dir, 'favicon.ico')
    if isfile(favicon_path):
        return FileResponse(favicon_path)
    print('[!] cant find favicon')
    return None


# Serve static files from the 'pages' directory
app.mount('/pages', StaticFiles(directory=pages_dir), name='pages')

if __name__ == '__main__':
    run("ManagerPanel:app", port=PORT, reload=True)
