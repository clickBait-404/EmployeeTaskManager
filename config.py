"""
config.py
---------
Central configuration for the Task Management System.
Edit the DB_CONFIG values to match your local MySQL setup.
"""

import os

# Flask secret key (used to sign session cookies).
# In production, set this via an environment variable instead of hardcoding it.
SECRET_KEY = os.environ.get("TMS_SECRET_KEY", "change-this-secret-key-in-production")

# MySQL database connection settings
DB_CONFIG = {
    "host": os.environ.get("TMS_DB_HOST", "localhost"),
    "user": os.environ.get("TMS_DB_USER", "root"),
    "password": os.environ.get("TMS_DB_PASSWORD", ""),
    "database": os.environ.get("TMS_DB_NAME", "task_management"),
}

# Fixed dropdown options for Task Title (per spec: dropdown, not free text)
TASK_TITLE_OPTIONS = [
    "Design UI",
    "Develop Backend",
    "Fix Bug",
    "Testing",
    "Deployment",
    "Documentation",
]
