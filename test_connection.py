from database.db_connection import get_connection

try:
    conn = get_connection()

    if conn.is_connected():
        print("Connected to Vireon database successfully!")

    conn.close()

except Exception as e:
    print("Database connection failed:")
    print(e)