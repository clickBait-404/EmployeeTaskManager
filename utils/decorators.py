"""
utils/decorators.py
--------------------
Reusable route decorators for session-based authentication and
role-based access control.
"""

from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """Redirect to login page if no user is logged in."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


def role_required(role):
    """Only allow access if the logged-in user's role matches `role`."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to continue.", "error")
                return redirect(url_for("auth.login"))
            if session.get("role") != role:
                flash("You do not have permission to access that page.", "error")
                # Send the user back to whatever dashboard matches their role
                if session.get("role") == "Admin":
                    return redirect(url_for("admin.admin_dashboard"))
                return redirect(url_for("employee.employee_dashboard"))
            return f(*args, **kwargs)
        return wrapper
    return decorator
