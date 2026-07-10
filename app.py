"""
app.py
------
Main entry point for the Task Management System (Flask, MVC structure).

Run with:
    python app.py

Make sure you have:
1. Created the MySQL database using database/task_management.sql
2. Updated config.py (or the TMS_DB_* environment variables) with your
   MySQL credentials
3. Installed dependencies from requirements.txt
"""

from flask import Flask
from config import SECRET_KEY

from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.employee_controller import employee_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register blueprints (controllers)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(employee_bp)


if __name__ == "__main__":
    app.run(debug=True)
