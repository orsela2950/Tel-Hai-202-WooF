import sqlite3
from datetime import datetime, timedelta
import os

PUNISHMENTS_DB_NAME = 'punishment_db.db'
current_dir = os.path.dirname(os.path.realpath(__file__))
PUNISHMENTS_DB_FULL_PATH = os.path.join(current_dir, PUNISHMENTS_DB_NAME)


def validate_table() -> None:
    """Validate that the databases exists and if not creating them."""
    # create the table
    with sqlite3.connect(PUNISHMENTS_DB_FULL_PATH) as conn:
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS strikes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
ip_address TEXT NOT NULL,
reason TEXT,
expiration_date DATETIME);""")
        conn.commit()


def clear_blacklist_history() -> None:
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
        @param ip_address: The IP address to check.

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
        ip_address: str,
        expiration_date: datetime,
        reason: str = "Not specified",  # Optional parameter with default value
        source: str = "Unknown",  # Optional parameter with default value
        conn: sqlite3.Connection = None  # Type hint for the database connection
) -> None:
    """Inserts a user into the blacklist table with optional reason and source.

    Args:
        - conn: The SQLite connection object. -
        @param ip_address: The IP address to blacklist.
        @param expiration_date: The date and time when the ban should expire.
        @param reason: An optional reason for blacklisting the IP address.
        @param source: An optional source of information for the blacklisting.
        @param conn:
    """

    def preform_insert(db_connection):
        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO blacklist (ip_address, reason, expiration_date, source) VALUES (?, ?, ?, ?)",
            (ip_address, reason, expiration_date, source),
        )
        db_connection.commit()

    if conn:
        preform_insert(conn)
    else:
        with sqlite3.connect(PUNISHMENTS_DB_NAME) as conn:
            preform_insert(conn)


def strike_user(
        ip_address: str,
        reason: str = "Not specified"
) -> None:
    """Adds a strike to the user, applies punishments based on existing strikes, and updates blacklist.

    Args:
        @param ip_address: The IP address of the user to strike.
        @param reason: An optional reason for the strike.
    """
    with sqlite3.connect(PUNISHMENTS_DB_NAME) as conn:
        # Insert strike:
        strike_expiration_date = datetime.now() + timedelta(weeks=2)
        conn.execute(
            """
            INSERT INTO strikes (ip_address, reason, expiration_date)
            VALUES (?, ?, ?)
            """,
            (ip_address, reason, strike_expiration_date)
        )
        conn.commit()

        # Count existing non-expired strikes:
        existing_strikes = conn.execute("SELECT COUNT(*) FROM strikes WHERE ip_address = ? AND expiration_date > ?",
                                        (ip_address, datetime.now())).fetchone()[0]

        # Determine expiration based on strike count:
        if existing_strikes == 1:
            expiration_date = datetime.now() + timedelta(hours=2)
            insert_blacklisted_user(ip_address, expiration_date, reason, conn=conn)
        elif existing_strikes == 2:
            expiration_date = datetime.now() + timedelta(days=2)
            insert_blacklisted_user(ip_address, expiration_date, reason, conn=conn)
        else:
            expiration_date = datetime.now() + (timedelta(days=365) * 1000)  # Make it +1000 years
            insert_blacklisted_user(ip_address, expiration_date, "Permanent ban due to repeated strikes",
                                    conn=conn)  # No expiration


validate_table()  # Always run this function to allow for proper work with the database
if __name__ == '__main__':
    # Use examples:
    # refresh_blacklist()  # Run this only when you want to clear punishments history (not a 'must')

    # insert_blacklisted_user("192.168.1.100", datetime.now() + timedelta(weeks=5), "Suspicious activity",
    # "WAF alert") insert_blacklisted_user("192.168.1.100", datetime.now() + timedelta(days=4), reason="Suspicious
    # activity", source="WAF alert") insert_blacklisted_user("192.168.1.100", datetime.now() + timedelta(hours=3),
    # reason="Suspicious activity") insert_blacklisted_user("192.168.1.100", datetime.now() + timedelta(minutes=2),
    # source="WAF alert") insert_blacklisted_user("192.168.1.100", datetime.now() + timedelta(seconds=1))

    # strike_user('192.168.1.100', 'L')
    strike_user('127.0.0.1', 'L')
    # Will return the ban with the furthest expiration date V
    # is_banned, ip, reason, expiration, source = check_ip_ban("127.0.0.1")
    print(check_ip_ban("127.0.0.1"))
