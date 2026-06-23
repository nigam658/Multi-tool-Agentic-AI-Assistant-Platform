from database import get_mysql


def create_user(
    email,
    password
):
    conn = get_mysql()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (
            email,
            password
        )
        VALUES (%s,%s)
        """,
        (
            email,
            password
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_user_by_email(email):

    conn = get_mysql()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = %s
        """,
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user