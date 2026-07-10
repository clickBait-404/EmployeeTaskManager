"""
controllers/auth_controller.py
--------------------------------
Handles login, logout, and the root redirect route.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.user_model import get_user_by_username
from mysql.connector import Error

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    """
    Root route. If already logged in, send the user to their dashboard.
    Otherwise, send them to the login page.
    """
    if "user_id" in session:
        if session.get("role") == "Admin":
            return redirect(url_for("admin.admin_dashboard"))
        return redirect(url_for("employee.employee_dashboard"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    GET  -> show the login form.
    POST -> validate credentials, start a session, and redirect by role.
    """
    if request.method == "GET":
        # If already logged in, skip straight to the right dashboard
        if "user_id" in session:
            if session.get("role") == "Admin":
                return redirect(url_for("admin.admin_dashboard"))
            return redirect(url_for("employee.employee_dashboard"))
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        flash("Username and password are required.", "error")
        return render_template("login.html")

    try:
        user = get_user_by_username(username)
    except Error:
        flash("Could not connect to the database. Please try again later.", "error")
        return render_template("login.html")

    if user is None or not check_password_hash(user["password"], password):
        flash("Invalid username or password.", "error")
        return render_template("login.html")

    # Credentials are valid -- start the session
    session["user_id"] = user["user_id"]
    session["username"] = user["username"]
    session["employee_name"] = user["employee_name"]
    session["role"] = user["role"]

    flash(f"Welcome, {user['employee_name']}!", "success")

    if user["role"] == "Admin":
        return redirect(url_for("admin.admin_dashboard"))
    return redirect(url_for("employee.employee_dashboard"))


@auth_bp.route("/logout")
def logout():
    """Clear the session and return to the login page."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
