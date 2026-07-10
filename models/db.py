"""
models/db.py
------------
Handles the raw MySQL connection using mysql.connector.
All other model files import get_connection() from here.
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def get_connection():
    """
    Opens and returns a new MySQL connection using settings from config.py.
    Raises mysql.connector.Error if the connection fails; callers should
    handle this with try/except so the app can show a friendly error
    instead of crashing.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
        )
        return connection
    except Error as err:
        # Let the calling controller decide how to present this error.
        raise err
