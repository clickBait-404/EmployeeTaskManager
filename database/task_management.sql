-- =====================================================================
-- Task Management System - Database Schema & Sample Data
-- =====================================================================

-- ------------------------------------------------------------
-- 1. Create Database
-- ------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS task_management;
USE task_management;

-- ------------------------------------------------------------
-- 2. Create Tables
-- ------------------------------------------------------------

-- Drop tables if they already exist (order matters due to FK)
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id       INT PRIMARY KEY AUTO_INCREMENT,
    username      VARCHAR(50) NOT NULL UNIQUE,
    password      VARCHAR(255) NOT NULL,
    employee_name VARCHAR(100) NOT NULL,
    role          ENUM('Admin','Employee') NOT NULL
);

CREATE TABLE tasks (
    task_id     INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    task_title  VARCHAR(200) NOT NULL,
    completed   BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- 3. Sample Users
-- ------------------------------------------------------------
-- Passwords are stored as werkzeug scrypt hashes (secure, not plaintext).
--
-- Admin login   -> Username: admin   | Password: admin123
-- Employee logins (all use the SAME password for convenience in dev/testing):
--   Username: rahul  | Password: emp123
--   Username: priya  | Password: emp123
--   Username: aman   | Password: emp123
--   Username: neha   | Password: emp123
--   Username: vikram | Password: emp123

INSERT INTO users (username, password, employee_name, role) VALUES
('admin', 'scrypt:32768:8:1$wPBrwlApM5Lb9Cjh$73e0732b6e6813ca953120a29191827e309be5f9357a954b666378ceee4c02c89c8a05ed04c36cf076de6225c5c78c2cc0d2c6f6c83a13050aa3f3ec641ee159', 'Administrator', 'Admin');

INSERT INTO users (username, password, employee_name, role) VALUES
('rahul',  'scrypt:32768:8:1$YlV6c5GEHCz7RZGX$5e04a0617d541a5911f3c08a6fdf63d792c2aca69d2f8cac4dcdcd42f4148f144d641b4258f86bfd821fd3635177f95ccc397ac2abcdb0bdf021ef4170ff6159', 'Rahul Sharma', 'Employee'),
('priya',  'scrypt:32768:8:1$YlV6c5GEHCz7RZGX$5e04a0617d541a5911f3c08a6fdf63d792c2aca69d2f8cac4dcdcd42f4148f144d641b4258f86bfd821fd3635177f95ccc397ac2abcdb0bdf021ef4170ff6159', 'Priya Verma', 'Employee'),
('aman',   'scrypt:32768:8:1$YlV6c5GEHCz7RZGX$5e04a0617d541a5911f3c08a6fdf63d792c2aca69d2f8cac4dcdcd42f4148f144d641b4258f86bfd821fd3635177f95ccc397ac2abcdb0bdf021ef4170ff6159', 'Aman Gupta', 'Employee'),
('neha',   'scrypt:32768:8:1$YlV6c5GEHCz7RZGX$5e04a0617d541a5911f3c08a6fdf63d792c2aca69d2f8cac4dcdcd42f4148f144d641b4258f86bfd821fd3635177f95ccc397ac2abcdb0bdf021ef4170ff6159', 'Neha Singh', 'Employee'),
('vikram', 'scrypt:32768:8:1$YlV6c5GEHCz7RZGX$5e04a0617d541a5911f3c08a6fdf63d792c2aca69d2f8cac4dcdcd42f4148f144d641b4258f86bfd821fd3635177f95ccc397ac2abcdb0bdf021ef4170ff6159', 'Vikram Rao', 'Employee');

-- ------------------------------------------------------------
-- 4. Sample Tasks
-- ------------------------------------------------------------
INSERT INTO tasks (employee_id, task_title, completed) VALUES
(2, 'Design UI', FALSE),
(2, 'Fix Bug', TRUE),
(3, 'Develop Backend', FALSE),
(4, 'Testing', FALSE),
(5, 'Deployment', TRUE),
(6, 'Documentation', FALSE);
