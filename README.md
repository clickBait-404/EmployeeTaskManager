# Task Management System

A full-stack Task Management System with **Admin** and **Employee** roles, built with:

- **Frontend:** HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Backend:** Python Flask (MVC folder structure)
- **Database:** MySQL

Admins can create and manage tasks assigned to employees. Employees can only view the tasks assigned to them.

---

## 1. Project Structure

```
TaskManagement/
│
├── app.py                     # Main Flask entry point (registers blueprints)
├── config.py                  # DB credentials, secret key, task title options
├── requirements.txt
├── README.md
│
├── models/                    # MODEL layer (all SQL lives here)
│   ├── db.py                  # mysql.connector connection helper
│   ├── user_model.py          # users table queries
│   └── task_model.py          # tasks table queries
│
├── controllers/                # CONTROLLER layer (Flask routes / blueprints)
│   ├── auth_controller.py     # /, /login, /logout
│   ├── admin_controller.py    # /admin, /add_task, /edit_task/<id>, /delete_task/<id>
│   └── employee_controller.py # /employee
│
├── utils/
│   └── decorators.py          # @login_required / @role_required guards
│
├── templates/                  # VIEW layer (Jinja2 templates)
│   ├── login.html
│   ├── admin.html
│   └── employee.html
│
├── static/
│   ├── css/style.css          # White background, black borders, minimalist
│   └── js/script.js           # Validation, edit modal, delete confirmation
│
└── database/
    └── task_management.sql    # CREATE DATABASE / TABLE + sample data
```

---

## 2. Prerequisites

- Python 3.9+
- MySQL Server 8.0+ (or MariaDB) running locally or accessible remotely
- `pip` for installing Python packages

---

## 3. Setup Instructions

### Step 1 — Clone / copy the project

Place the `TaskManagement/` folder wherever you'd like to run it from.

### Step 2 — Create a virtual environment (recommended)

```bash
cd TaskManagement
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Create the database

Run the provided SQL script against your MySQL server:

```bash
mysql -u root -p < database/task_management.sql
```

This will:
- Create the `task_management` database
- Create the `users` and `tasks` tables
- Insert 1 admin account and 5 employee accounts
- Insert 6 sample tasks

### Step 5 — Configure database credentials

Open `config.py` and update the `DB_CONFIG` dictionary with your MySQL username/password, **or** set environment variables instead of editing the file:

```bash
export TMS_DB_HOST=localhost
export TMS_DB_USER=root
export TMS_DB_PASSWORD=yourpassword
export TMS_DB_NAME=task_management
export TMS_SECRET_KEY=some-random-secret-string
```

### Step 6 — Run the app

```bash
python app.py
```

The app will start on **http://127.0.0.1:5000**.

---

## 4. Demo Login Credentials

| Role     | Username | Password |
|----------|----------|----------|
| Admin    | admin    | admin123 |
| Employee | rahul    | emp123   |
| Employee | priya    | emp123   |
| Employee | aman     | emp123   |
| Employee | neha     | emp123   |
| Employee | vikram   | emp123   |

Passwords are stored as **werkzeug scrypt hashes** in the database (not plain text), and verified with `check_password_hash()` on login.

---

## 5. Feature Overview

### Login
- Single login form (username + password) for both roles.
- Session-based authentication (`flask.session`).
- On success, redirects by role: Admin → `/admin`, Employee → `/employee`.

### Admin Dashboard (`/admin`)
- **Create Task** card with:
  - **Task ID** — read-only "Auto Generated" field (MySQL `AUTO_INCREMENT`, never sent from the client)
  - **Employee Name** — dropdown populated dynamically from `users` where `role = 'Employee'`
  - **Task Title** — dropdown with fixed options (Design UI, Develop Backend, Fix Bug, Testing, Deployment, Documentation)
  - **Completed** — dropdown (`False` / `True`, default `False`)
  - **Submit** button (bottom-right) — inserts into DB, shows a flash success message, and clears the form on reload
- **All Tasks** table below the form: Task ID, Employee Name, Task Title, Completed, Created Date, Actions (Edit / Delete)
  - **Edit** opens a modal, pre-filled via an AJAX `GET /edit_task/<id>` call; saving submits `POST /edit_task/<id>`
  - **Delete** asks for confirmation (`window.confirm`) before submitting `POST /delete_task/<id>`
- **Right-side box** showing "Logged in as: Admin" and the admin's name.

### Employee Dashboard (`/employee`)
- Read-only table: Task ID, Task Title, Completed — showing **only** tasks assigned to the logged-in employee.
- No create/edit/delete controls.
- "Logged in as: Employee" side box + Logout button.

### Validation
- **Client-side (JavaScript):** required-field checks on Employee, Task Title, and Completed before form submission (both Add and Edit forms), plus delete confirmation.
- **Server-side (Flask):** every form field is re-validated in the controller before touching the database, so the API can't be bypassed by disabling JS.

### Security
- All SQL queries use **parameterized queries** (`%s` placeholders via `mysql.connector`) — no string-concatenated SQL anywhere.
- Passwords hashed with `werkzeug.security.generate_password_hash` / `check_password_hash`.
- Routes protected with `@login_required` / `@role_required` decorators — an Employee cannot open `/admin` or POST to `/add_task`, `/edit_task/<id>`, or `/delete_task/<id>`, and vice versa.
- `task_id` is **never** accepted as input from the client on create or edit — it's always DB-generated.

---

## 6. Routes Summary

| Method | Route                | Access         | Purpose                                  |
|--------|-----------------------|----------------|-------------------------------------------|
| GET    | `/`                   | Public         | Redirect to login or dashboard            |
| GET/POST | `/login`             | Public         | Login form + credential check             |
| GET    | `/logout`             | Logged in      | Clear session                             |
| GET    | `/admin`              | Admin only     | Admin dashboard (form + task table)       |
| POST   | `/add_task`           | Admin only     | Create a new task                         |
| GET/POST | `/edit_task/<id>`   | Admin only     | GET = fetch task JSON, POST = apply edit  |
| POST   | `/delete_task/<id>`   | Admin only     | Delete a task                             |
| GET    | `/employee`           | Employee only  | Employee dashboard (own tasks only)       |

---

## 7. Notes

- The app runs in Flask's debug mode by default (`app.run(debug=True)`) for development convenience. **Turn this off in production.**
- `SECRET_KEY` and DB credentials should be set via environment variables in any real deployment — never commit real secrets to source control.
- The UI intentionally uses a minimalist white background with solid black (2px) borders and no gradients, per the design spec — no CSS frameworks are used anywhere.
