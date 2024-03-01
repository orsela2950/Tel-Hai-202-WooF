import sqlite3, re
from fastapi import HTTPException
from os.path import join, abspath, dirname

program_dir = abspath(dirname(__file__))
db_path = join(program_dir, '..', 'WoofSourceFiles/punishment_db.db')
# Regular expression for validating an IPv4 address
ip_address_pattern = re.compile(
    r"^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])$")


def add_blacklist_user(ip_address: str, reason: str, expiration_date, source: str):
    # Validate IP address using regex
    if not re.match(ip_address_pattern, ip_address):
        raise HTTPException(status_code=400, detail="Invalid IP address format")

    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO blacklist (ip_address, reason, expiration_date, source) VALUES (?, ?, ?, ?)",
            (ip_address, reason, expiration_date, source),
        )
        db_connection.commit()


def get_blacklist():
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

        return blacklist_data


def delete_blacklist_row(row_id: int):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Delete the row with the specified ID from the blacklist table
        cursor.execute("DELETE FROM blacklist WHERE id = ?", (row_id,))
        conn.commit()
        cursor.execute("DELETE FROM strikes WHERE id = ?", (row_id,))
        conn.commit()
