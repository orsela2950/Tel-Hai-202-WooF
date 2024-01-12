import os
import sqlite3
from datetime import datetime, timedelta

PUNISHMENTS_DB_NAME = 'waf_blacklist.db'


def refresh_blacklist() -> None:
    """Updates expiration dates for expired bans in the blacklist table.
    No need to use every time, only for cleaning the database once in a while
    """
    with sqlite3.connect(PUNISHMENTS_DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE blacklist
            SET expiration_date = ?
            WHERE expiration_date <= ?
            """,
            (datetime.now(), datetime.now())
        )
        conn.commit()


def check_ip_ban(ip_address: str) -> tuple:
    """Checks if an IP address is banned, returning ban information if found and active.

    Args:
        ip_address: The IP address to check.

    Returns:
        A tuple containing (is_banned, ip_address, reason, strikes, expiration_date, ban)
        if the IP is banned and the ban is active, otherwise (False, None, None, None, None, None).
    """
    with sqlite3.connect(PUNISHMENTS_DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM blacklist
            WHERE ip_address = ?
            AND 
            (expiration_date > ? OR ban = ?) 
            ORDER BY expiration_date DESC
            LIMIT 1
            """,
            (ip_address, datetime.now(),True)  # Check for current time
        )

        ban_data = cursor.fetchone()

        if ban_data:
            is_banned = True
            reason = ban_data[2]
            strikes = ban_data[3]
            expiration_date = ban_data[4]
            ban = ban_data[5]
            return is_banned, ip_address, reason, strikes, expiration_date, ban
        else:
            return False, None, None, None, None, None

def remove_user_ban(ip_address: str) -> None:
    """Removes ban for a specific user.

    Args:
        ip_address: The IP address to remove the ban for.
    """
    with sqlite3.connect(PUNISHMENTS_DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE blacklist
            SET ban = ?,
            expiration_date = ?,
            WHERE ip_address = ?
            """,
            (False,datetime.now(),ip_address)
        )
        conn.commit()





def insert_blacklisted_user(
    ip_address: str,
    expiration_date: datetime,
    new_reason: str = "Not specified"
) -> None:
    """Inserts a user into the blacklist table with optional reason and source.

    Args:
        ip_address: The IP address to blacklist.
        expiration_date: The date and time when the ban should expire.
        new_reason: An optional new reason for blacklisting the IP address.
    """

    with sqlite3.connect(PUNISHMENTS_DB_NAME) as conn:
        cursor = conn.cursor()

        # Check if the user is already in the blacklist
        cursor.execute("SELECT * FROM blacklist WHERE ip_address = ?", (ip_address,))
        existing_user = cursor.fetchone()

        if existing_user:
             # User already exists, update the reasons, strikes, and expiration_date
            current_reason = existing_user[2]
            current_strikes = existing_user[3] + 1
            current_expiration_date = existing_user[4]
            current_ban_status = existing_user[5]

            updated_reasons = f"{current_reason}, {new_reason}"

            # Update expiration date to be the sum of both expiration dates
            updated_expiration_date = current_expiration_date + (expiration_date - datetime.now())

            cursor.execute(
                "UPDATE blacklist SET reason = ?, strikes = ?, expiration_date = ? WHERE ip_address = ?",
                (updated_reasons, current_strikes, updated_expiration_date, ip_address),
            )
            # Check if the user has reached 3 strikes and update ban status
            if current_strikes >= 3 and not current_ban_status:
                cursor.execute(
                    "UPDATE blacklist SET strike = ?,ban = ? WHERE ip_address = ?",
                    (0,True,ip_address),
                )
        else:
            # User doesn't exist, insert a new record
            cursor.execute(
                "INSERT INTO blacklist (ip_address, reason, strikes, expiration_date, ban) VALUES (?, ?, ?, ?, ?)",
                (ip_address, new_reason, 1, expiration_date, False),
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
  strikes INTEGER,
  expiration_date DATETIME NOT NULL,
  ban BOOL);""")

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