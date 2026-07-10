"""
models/task_model.py
----------------------
All database operations related to the `tasks` table.
Uses parameterized queries throughout to prevent SQL injection.
"""

from models.db import get_connection


def get_all_tasks():
    """
    Fetch all tasks joined with employee_name, ordered by newest first.
    Used to render the admin dashboard task table.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT t.task_id, t.employee_id, u.employee_name,
                   t.task_title, t.completed, t.created_at
            FROM tasks t
            JOIN users u ON t.employee_id = u.user_id
            ORDER BY t.task_id DESC
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_tasks_by_employee(employee_id):
    """
    Fetch only the tasks assigned to a specific employee.
    Used to render the employee dashboard (they only see their own tasks).
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT task_id, task_title, completed, created_at
            FROM tasks
            WHERE employee_id = %s
            ORDER BY task_id DESC
            """,
            (employee_id,)
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_task_by_id(task_id):
    """Fetch a single task row by task_id. Returns a dict or None."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT task_id, employee_id, task_title, completed, created_at "
            "FROM tasks WHERE task_id = %s",
            (task_id,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def create_task(employee_id, task_title, completed):
    """
    Insert a new task row. task_id is AUTO_INCREMENT (never supplied by
    the client). Returns the new task_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tasks (employee_id, task_title, completed) "
            "VALUES (%s, %s, %s)",
            (employee_id, task_title, completed)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()


def update_task(task_id, employee_id, task_title, completed):
    """
    Update an existing task's employee, title, and completed status.
    task_id itself is never editable (per spec).
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE tasks
            SET employee_id = %s, task_title = %s, completed = %s
            WHERE task_id = %s
            """,
            (employee_id, task_title, completed, task_id)
        )
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()


def delete_task(task_id):
    """Delete a task row by task_id. Returns number of rows affected."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()
