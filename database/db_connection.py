import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",   # change if needed
    "database": "vireon"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)