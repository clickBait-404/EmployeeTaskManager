"""
models/user_model.py
---------------------
All database operations related to the `users` table.
Uses parameterized queries throughout to prevent SQL injection.
"""

from models.db import get_connection


def get_user_by_username(username):
    """
    Fetch a single user row by username. Returns a dict or None.
    Used during login to verify credentials.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT user_id, username, password, employee_name, role "
            "FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        return user
    finally:
        cursor.close()
        conn.close()


def get_all_employees():
    """
    Fetch all users with role = 'Employee'.
    Used to populate the Employee Name dropdown on the admin dashboard.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT user_id, employee_name FROM users "
            "WHERE role = 'Employee' ORDER BY employee_name ASC"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_user_by_id(user_id):
    """Fetch a single user row by user_id. Returns a dict or None."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT user_id, username, employee_name, role "
            "FROM users WHERE user_id = %s",
            (user_id,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
