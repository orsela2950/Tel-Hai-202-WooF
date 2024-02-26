from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from uvicorn import run
from os.path import join, abspath, dirname, isfile
import json
import sqlite3
# Import custom modules
import serverInfoWrite
import re

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


# Regular expression for validating an IPv4 address
ip_address_pattern = re.compile(
    r"^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\. "
    r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\. "
    r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\. "
    r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
)


@app.post("/add-blacklist-row")
async def add_blacklist_row(request_data: dict):
    # Extract data from the request
    ip_address = request_data.get("ipAddress")
    reason = request_data.get("reason")
    expiration_date = request_data.get("expirationDate")
    source = request_data.get("source")

    # Validate IP address using regex
    if not re.match(ip_address_pattern, ip_address):
        raise HTTPException(status_code=400, detail="Invalid IP address format")

    # Perform validation and insert the new row into the database
    try:
        # Perform SQL validation here if needed

        # Use parameterized query to prevent SQL injection
        with sqlite3.connect(db_path) as db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                "INSERT INTO blacklist (ip_address, reason, expiration_date, source) VALUES (?, ?, ?, ?)",
                (ip_address, reason, expiration_date, source),
            )
            db_connection.commit()

    except sqlite3.Error as sql_error:
        raise HTTPException(status_code=500, detail=f"Error executing SQL query: {sql_error}")

    return JSONResponse(content={"message": "Row added successfully"})


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


@app.get('/blacklist')
async def get_blacklist():
    try:
        # Connect to the SQLite database
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Fetch all rows from the blacklist table
            cursor.execute("SELECT * FROM blacklist")
            rows = cursor.fetchall()

            # Convert rows to a list of dictionaries
            blacklist_data = []
            for row in rows:
                entry = {
                    'id': row[0],
                    'ip_address': row[1],
                    'reason': row[2],
                    'expiration_date': row[3],
                    'source': row[4]
                }
                blacklist_data.append(entry)

            return JSONResponse(content={'blacklist': blacklist_data})

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error fetching blacklist data: {e}')


# Add a new endpoint to handle row deletion
@app.delete('/delete/{row_id}')
async def delete_row(row_id: int):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Delete the row with the specified ID from the blacklist table
            cursor.execute("DELETE FROM blacklist WHERE id = ?", (row_id,))
            conn.commit()
            cursor.execute("DELETE FROM strikes WHERE id = ?", (row_id,))
            conn.commit()

        return JSONResponse(content={'message': 'Row deleted successfully'})

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error deleting row: {e}')


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
