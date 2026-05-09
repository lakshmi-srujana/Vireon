import hashlib
from database.db_connection import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login_user(username, password):

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        hashed_password = hash_password(password)

        query = """
        SELECT *
        FROM users
        WHERE username = %s
        AND password_hash = %s
        AND is_active = TRUE
        """

        cursor.execute(query, (username, hashed_password))

        user = cursor.fetchone()

        conn.close()

        return user

    except Exception as e:
        print("Login Error:", e)
        return None