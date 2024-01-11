import os
import sqlite3
from datetime import datetime, timedelta

PUNISHMENTS_DB_NAME = 'waf_blacklist.db'


def refresh_blacklist() -> None:
    """Removes expired bans from the blacklist table.
    No need to use everytime, only for cleaning the database once in a while
    """
    with sqlite3.connect(PUNISHMENTS_DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM blacklist
            WHERE expiration_date <= ?
            """,
            (datetime.now(),)
        )
        conn.commit()


def check_ip_ban(ip_address: str) -> tuple:
    """Checks if an IP address is banned, returning ban information if found and active.

    Args:
        conn: The SQLite connection object.
        ip_address: The IP address to check.

    Returns:
        A tuple containing (is_banned, ip_address, reason, expiration_date, source)
        if the IP is banned and the ban is active, otherwise (False, None, None, None, None).
    """
    with sqlite3.connect(PUNISHMENTS_DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM blacklist
            WHERE ip_address = ?
            AND expiration_date > ?
            ORDER BY expiration_date DESC
            LIMIT 1
            """,
            (ip_address, datetime.now())  # Check for current time
        )

        ban_data = cursor.fetchone()

        if ban_data:
            is_banned = True
            reason = ban_data[2]
            expiration_date = ban_data[3]
            source = ban_data[4]
            return is_banned, ip_address, reason, expiration_date, source
        else:
            return False, None, None, None, None


def insert_blacklisted_user(
    #conn: sqlite3.Connection,  # Type hint for the database connection
    ip_address: str,
    expiration_date: datetime,
    reason: str = "Not specified",  # Optional parameter with default value
    source: str = "Unknown"  # Optional parameter with default value
) -> None:
    """Inserts a user into the blacklist table with optional reason and source.

    Args:
        - conn: The SQLite connection object. -
        ip_address: The IP address to blacklist.
        expiration_date: The date and time when the ban should expire.
        reason: An optional reason for blacklisting the IP address.
        source: An optional source of information for the blacklisting.
    """

    with sqlite3.connect(PUNISHMENTS_DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO blacklist (ip_address, reason, expiration_date, source) VALUES (?, ?, ?, ?)",
            (ip_address, reason, expiration_date, source),
        )
        conn.commit()


def validateTable() -> None:
    """Validate that the databases exists and if not creating them."""
    if not os.path.exists("file.txt"):
        # create the table
        with sqlite3.connect(PUNISHMENTS_DB_NAME) as conn:
            # create all tables for the woof to work properly
            cursor = conn.cursor()
            # blacklist table:
            cursor.execute("""CREATE TABLE IF NOT EXISTS blacklist (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ip_address TEXT NOT NULL,
  reason TEXT,
  expiration_date DATETIME NOT NULL,
  source TEXT);""")

            # strikes table: future use
            cursor.execute("""""")
            conn.commit()

validateTable()  # Always run this function to allow for proper work with the database
if __name__ == '__main__':
    # Use examples:
    # refresh_blacklist()  # Run this only when you want to clear punishments history (not a 'must')

    insert_blacklisted_user("192.168.1.100", datetime.now() + timedelta(weeks=5), "Suspicious activity", "WAF alert")
    insert_blacklisted_user("192.168.1.100", datetime.now() + timedelta(days=4), reason="Suspicious activity", source="WAF alert")
    insert_blacklisted_user("192.168.1.100", datetime.now() + timedelta(hours=3), reason="Suspicious activity")
    insert_blacklisted_user("192.168.1.100", datetime.now() + timedelta(minutes=2), source="WAF alert")
    insert_blacklisted_user("192.168.1.100", datetime.now() + timedelta(seconds=1))

    # Will return the ban with the furthest expiration date V
    is_banned, ip, reason, expiration, source = check_ip_ban("192.168.1.100")
    print(check_ip_ban("192.168.31.100"))