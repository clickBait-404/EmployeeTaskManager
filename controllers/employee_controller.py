"""
controllers/employee_controller.py
-------------------------------------
Handles the employee dashboard. Employees can only VIEW tasks
assigned to them -- no create/edit/delete access.
"""

from flask import Blueprint, render_template, session, flash
from mysql.connector import Error

from models.task_model import get_tasks_by_employee
from utils.decorators import role_required

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/employee")
@role_required("Employee")
def employee_dashboard():
    """Render the employee dashboard showing only this user's tasks."""
    try:
        tasks = get_tasks_by_employee(session["user_id"])
    except Error:
        flash("Database error while loading your tasks.", "error")
        tasks = []

    return render_template(
        "employee.html",
        tasks=tasks,
        employee_name=session.get("employee_name"),
    )
