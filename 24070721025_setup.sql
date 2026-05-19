-- ============================================
-- VIREON DATABASE SETUP
-- ============================================

CREATE DATABASE vireon
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE vireon;

-- ============================================
-- STUDENTS TABLE
-- ============================================

CREATE TABLE students (

id INT AUTO_INCREMENT PRIMARY KEY,

roll_no VARCHAR(20)
NOT NULL UNIQUE,

full_name VARCHAR(100)
NOT NULL,

department VARCHAR(50),

year INT,

cgpa DECIMAL(3,2),

attendance DECIMAL(5,2),

email VARCHAR(100),

phone VARCHAR(15),

created_at TIMESTAMP
DEFAULT CURRENT_TIMESTAMP,

UNIQUE(email),

CHECK(year BETWEEN 1 AND 4),

CHECK(cgpa BETWEEN 0 AND 10),

CHECK(attendance BETWEEN 0 AND 100)

);

CREATE INDEX idx_roll_no
ON students(roll_no);

CREATE INDEX idx_department
ON students(department);

-- ============================================
-- FACULTY TABLE
-- ============================================

CREATE TABLE faculty(

id INT AUTO_INCREMENT PRIMARY KEY,

faculty_id VARCHAR(20)
UNIQUE,

full_name VARCHAR(100),

department VARCHAR(50),

designation VARCHAR(50),

email VARCHAR(100),

phone VARCHAR(15),

created_at TIMESTAMP
DEFAULT CURRENT_TIMESTAMP,

UNIQUE(email),

CHECK(
designation IN
(
'Professor',
'Associate Professor',
'Assistant Professor',
'Jr. Professor'
)
)

);

-- ============================================
-- USERS TABLE
-- ============================================

CREATE TABLE users(

id INT AUTO_INCREMENT PRIMARY KEY,

username VARCHAR(50)
NOT NULL UNIQUE,

password_hash VARCHAR(255)
COLLATE utf8mb4_bin
NOT NULL,

role ENUM(
'admin',
'faculty',
'student'
),

linked_id VARCHAR(20),

is_active BOOLEAN DEFAULT TRUE,

created_at TIMESTAMP
DEFAULT CURRENT_TIMESTAMP

);

CREATE INDEX idx_username
ON users(username);

-- ============================================
-- AUDIT LOG TABLE
-- ============================================

CREATE TABLE audit_logs(

log_id INT AUTO_INCREMENT PRIMARY KEY,

action_type VARCHAR(20),

student_roll VARCHAR(20),

performed_by VARCHAR(50),

username VARCHAR(50),

role VARCHAR(20),

action_time TIMESTAMP
DEFAULT CURRENT_TIMESTAMP

);

-- ============================================
-- ATTENDANCE ALERTS
-- ============================================

CREATE TABLE attendance_alerts(

alert_id INT AUTO_INCREMENT PRIMARY KEY,

roll_no VARCHAR(20),

full_name VARCHAR(100),

attendance DECIMAL(5,2),

alert_message VARCHAR(255),

created_at TIMESTAMP
DEFAULT CURRENT_TIMESTAMP

);

-- ============================================
-- SAMPLE DATA
-- ============================================

INSERT INTO students
(
roll_no,
full_name,
department,
year,
cgpa,
attendance,
email,
phone
)

VALUES

('201',
'Aarav Sharma',
'CSE',
2,
8.76,
88,
'aarav@gmail.com',
'9876543201');

-- ============================================
-- VIEWS
-- ============================================

CREATE VIEW top_students AS

SELECT
roll_no,
full_name,
department,
cgpa

FROM students

ORDER BY cgpa DESC;


CREATE VIEW department_summary AS

SELECT

department,

AVG(cgpa)
AS average_cgpa,

AVG(attendance)
AS average_attendance

FROM students

GROUP BY department;


CREATE VIEW low_attendance AS

SELECT

roll_no,
full_name,
attendance

FROM students

WHERE attendance<75;


CREATE VIEW faculty_summary AS

SELECT

department,

COUNT(*)
AS faculty_count

FROM faculty

GROUP BY department;

-- ============================================
-- GRANT STATEMENTS
-- ============================================

GRANT ALL PRIVILEGES
ON vireon.*
TO 'admin_user'@'localhost';

GRANT SELECT,INSERT,UPDATE
ON vireon.students
TO 'faculty_user'@'localhost';

GRANT SELECT
ON vireon.students
TO 'student_user'@'localhost';

FLUSH PRIVILEGES;