import mysql.connector


def log_audit(
    action_type,
    performed_by,
    username,
    role
):

    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="vireon"
        )

        cursor = connection.cursor()

        query = """
        INSERT INTO audit_logs
        (
        action_type,
        performed_by,
        username,
        role
        )
        VALUES
        (%s, %s, %s, %s)
        """

        values = (
            action_type,
            performed_by,
            username,
            role
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

    except Exception as e:

        print(
            "Audit Error:",
            e
        )

    finally:

        cursor.close()

        connection.close()