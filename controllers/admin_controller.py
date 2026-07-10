"""
controllers/admin_controller.py
---------------------------------
Handles the admin dashboard and all task CRUD operations
(add_task, edit_task/<id>, delete_task/<id>).
Only accessible to users with role = 'Admin'.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from mysql.connector import Error

from models.user_model import get_all_employees
from models.task_model import (
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
)
from utils.decorators import role_required
from config import TASK_TITLE_OPTIONS

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@role_required("Admin")
def admin_dashboard():
    """Render the admin dashboard: task form + full task table."""
    try:
        employees = get_all_employees()
        tasks = get_all_tasks()
    except Error:
        flash("Database error while loading the dashboard.", "error")
        employees, tasks = [], []

    return render_template(
        "admin.html",
        employees=employees,
        tasks=tasks,
        task_titles=TASK_TITLE_OPTIONS,
        employee_name=session.get("employee_name"),
    )


@admin_bp.route("/add_task", methods=["POST"])
@role_required("Admin")
def add_task():
    """
    Insert a new task. task_id is never accepted from the client --
    MySQL AUTO_INCREMENT generates it.
    Validates all required fields server-side (in addition to the
    client-side JS validation) before touching the database.
    """
    employee_id = request.form.get("employee_id", "").strip()
    task_title = request.form.get("task_title", "").strip()
    completed_raw = request.form.get("completed", "").strip()

    # ---- Server-side validation ----
    errors = []
    if not employee_id:
        errors.append("Please select an employee.")
    if not task_title or task_title not in TASK_TITLE_OPTIONS:
        errors.append("Please select a valid task.")
    if completed_raw not in ("True", "False"):
        errors.append("Please select a completed status.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("admin.admin_dashboard"))

    completed = completed_raw == "True"

    try:
        create_task(int(employee_id), task_title, completed)
        flash("Task added successfully.", "success")
    except Error:
        flash("Database error while adding the task.", "error")

    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@role_required("Admin")
def edit_task(task_id):
    """
    GET  -> return the task's current data as JSON (used to pre-fill
            the edit form in the modal via JS fetch).
    POST -> apply the edit (employee, task title, completed status).
            task_id itself is never editable.
    """
    if request.method == "GET":
        try:
            task = get_task_by_id(task_id)
        except Error:
            return jsonify({"error": "Database error"}), 500

        if task is None:
            return jsonify({"error": "Task not found"}), 404

        # Convert datetime to string for JSON serialization
        task["created_at"] = str(task["created_at"])
        return jsonify(task)

    # POST -- apply the update
    employee_id = request.form.get("employee_id", "").strip()
    task_title = request.form.get("task_title", "").strip()
    completed_raw = request.form.get("completed", "").strip()

    errors = []
    if not employee_id:
        errors.append("Please select an employee.")
    if not task_title or task_title not in TASK_TITLE_OPTIONS:
        errors.append("Please select a valid task.")
    if completed_raw not in ("True", "False"):
        errors.append("Please select a completed status.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("admin.admin_dashboard"))

    completed = completed_raw == "True"

    try:
        existing = get_task_by_id(task_id)
        if existing is None:
            flash("Task not found.", "error")
            return redirect(url_for("admin.admin_dashboard"))

        update_task(task_id, int(employee_id), task_title, completed)
        flash("Task updated successfully.", "success")
    except Error:
        flash("Database error while updating the task.", "error")

    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/delete_task/<int:task_id>", methods=["POST"])
@role_required("Admin")
def delete_task_route(task_id):
    """Delete a task. Confirmation is handled client-side in JS."""
    try:
        rows_affected = delete_task(task_id)
        if rows_affected:
            flash("Task deleted successfully.", "success")
        else:
            flash("Task not found.", "error")
    except Error:
        flash("Database error while deleting the task.", "error")

    return redirect(url_for("admin.admin_dashboard"))
