-- =========================================
-- CREATE DATABASE
-- =========================================

CREATE DATABASE IF NOT EXISTS vireon
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE vireon;

-- =========================================
-- USERS TABLE
-- =========================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50)
    NOT NULL UNIQUE,

    password_hash VARCHAR(255)
    NOT NULL,

    role ENUM('admin', 'faculty', 'student')
    NOT NULL,

    is_active BOOLEAN
    DEFAULT TRUE,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    CHECK (role IN ('admin', 'faculty', 'student'))
);

-- =========================================
-- STUDENTS TABLE
-- =========================================

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100)
    NOT NULL,

    department VARCHAR(50)
    NOT NULL,

    marks DECIMAL(5,2)
    NOT NULL,

    user_id INT UNIQUE,

    enrolled_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    CHECK (marks BETWEEN 0 AND 100),

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);

-- =========================================
-- AUDIT LOG TABLE
-- =========================================

CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,

    action VARCHAR(100)
    NOT NULL,

    details TEXT,

    timestamp TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE SET NULL
);

-- =========================================
-- INDEXES
-- =========================================

CREATE INDEX idx_username
ON users(username);

CREATE INDEX idx_department
ON students(department);

CREATE INDEX idx_marks
ON students(marks);