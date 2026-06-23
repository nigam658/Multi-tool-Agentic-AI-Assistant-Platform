import requests
import re

from reminder_tool.reminder_repository import get_active_reminders, update_status_reminder, get_user_email
from email_tool.email_service import send_email


def get_myntra_price(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(e)
        return None

    print("Status Code:", response.status_code)

    html = response.text

    match = re.search(
        r'"discountedPrice":(\d+)',
        html
    )

    if match:
        return int(match.group(1))

    return None


def check_prices():

    reminders = get_active_reminders()

    for reminder in reminders:
        print(reminder)

        current_price = get_myntra_price(
            reminder["product_url"]
        )

        if current_price is None:
            print("Failed to get price")
            continue 

        if current_price <= reminder["target_price"]:

            email = get_user_email(
                reminder["user_id"]
            )

            if not email:
                continue

            send_email(
                recipient=email,
                subject="Price Drop Alert",
                body=f"""
                Product price has dropped.

                Current Price: Rs {current_price}
                Target Price: Rs {reminder['target_price']}

                Product URL:
                {reminder['product_url']}
                """
                )
            
            update_status_reminder(reminder["id"])

            print("Email Sent")

if __name__ == "__main__":
    from apscheduler.schedulers.blocking import BlockingScheduler
    print("Price checker started...")
    scheduler = BlockingScheduler()

    scheduler.add_job(
        check_prices,
        "interval",
        minutes=30
    )

    scheduler.start()