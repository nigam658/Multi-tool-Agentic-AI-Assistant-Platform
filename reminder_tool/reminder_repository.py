from database import get_mysql


def save_reminder(
    user_id,
    product_url,
    target_price
):

    conn = get_mysql()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reminders
        (
            user_id,
            product_url,
            target_price
        )
        VALUES (%s,%s,%s)
        """,
        (
            user_id,
            product_url,
            target_price
        )
    )
    conn.commit() 
    reminder_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return reminder_id


def get_user_reminders(user_id):

    conn = get_mysql()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            product_url,
            target_price
        FROM reminders
        WHERE user_id = %s
        """,
        (user_id,)
    )

    reminders = cursor.fetchall()

    cursor.close()
    conn.close()

    return reminders


def update_reminder_price(
    reminder_id,
    target_price
):

    conn = get_mysql()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE reminders
        SET target_price = %s
        WHERE id = %s
        """,
        (
            target_price,
            reminder_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return True


def delete_reminder(reminder_id):

    conn = get_mysql()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM reminders
        WHERE id = %s
        """,
        (reminder_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return True