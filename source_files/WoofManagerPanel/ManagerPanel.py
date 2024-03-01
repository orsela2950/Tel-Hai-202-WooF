from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from os.path import join, abspath, dirname, isfile
from sqlite3 import Error as sqlite3_err
from uvicorn import run
import json
# custom modules
import serverInfoWrite
import punishmentManager

PORT = 20343
# Ip is the loopback ip localhost/127.0.0.1

# Get program dir and path for use
program_dir = abspath(dirname(__file__))
pages_dir = join(program_dir, 'pages')
json_path = join(program_dir, '..', 'WoofSourceFiles/server_properties.json')
db_path = join(program_dir, '..', 'WoofSourceFiles/punishment_db.db')
logs_dir = join(program_dir, '..', 'logs')
logs_path = join(logs_dir, 'main.toml')
security_logs_path = join(logs_dir, 'security.toml')

# Create the FastAPI instance
app = FastAPI()


@app.get('/')
async def root():
    # Redirect to /pages/main.html
    return RedirectResponse(url='/pages/main.html')


@app.post("/add_blacklist_row")
async def add_blacklist_row(request_data: dict):
    # Extract data from the request
    ip_address = request_data.get("ipAddress")
    reason = request_data.get("reason")
    expiration_date = request_data.get("expirationDate")
    source = 'Manager manual ban'
    try:
        punishmentManager.add_blacklist_user(ip_address, reason, expiration_date, source)
    except sqlite3_err as sql_error:
        print(sql_error)
        raise HTTPException(status_code=500, detail=f"Error executing SQL query: {sql_error}")


@app.post('/submit-settings')
async def submit_settings(request: Request):
    form_data = await request.json()
    serverInfoWrite.set_settings_json_argument(form_data)


@app.post('/submit-rules')
async def submit_rules(request: Request):
    form_data = await request.json()
    serverInfoWrite.set_rules_json_argument(form_data)


@app.get('/check-switches')
async def ret_switches():
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
async def ret_settings():
    try:
        with open(json_path, 'r') as f:
            existing_data = json.load(f)

        del existing_data['rules']
        return JSONResponse(content=existing_data)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error fetching switch states: {e}')


@app.get('/logs')
async def ret_logs():
    return FileResponse(logs_path)


@app.get('/security_logs')
async def ret_security_logs():
    return FileResponse(security_logs_path)


@app.get('/blacklist')
async def get_blacklist():
    try:
        return JSONResponse(content={'blacklist': punishmentManager.get_blacklist()})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error fetching blacklist data: {e}')


@app.delete('/blacklist/{row_id}')
async def delete_row(row_id: int):
    try:
        punishmentManager.delete_blacklist_row(row_id)
        return JSONResponse(content={'message': 'Row deleted successfully'})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error deleting row: {e}')


@app.get('/favicon.ico')
async def favicon():
    favicon_path = join(program_dir, 'favicon.ico')
    if isfile(favicon_path):
        return FileResponse(favicon_path)
    print('[!] cant find favicon')
    return None


# Serve static files from the 'pages' directory
app.mount('/pages', StaticFiles(directory=pages_dir), name='pages')

if __name__ == '__main__':
    run("ManagerPanel:app", port=PORT, reload=True)
