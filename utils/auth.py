import hashlib
import mysql.connector


def login_user(username, password):

    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="vireon"
        )

        cursor = connection.cursor(dictionary=True)

        # ---------- HASH ENTERED PASSWORD ---------- #

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        # ---------- CHECK USER ---------- #

        query = """
        SELECT *
        FROM users
        WHERE username = %s
        AND password_hash = %s
        """

        values = (
            username,
            hashed_password
        )

        cursor.execute(
            query,
            values
        )

        user = cursor.fetchone()

        return user

    except Exception as e:

        print("Login Error:", e)

        return None

    finally:

        cursor.close()

        connection.close()