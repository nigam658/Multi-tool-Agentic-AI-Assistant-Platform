import json
from ai_client import client

from reminder_tool.reminder_repository import save_reminder, get_user_reminders
from session_manager import sessions
from reminder_tool.reminder_ai_services import extract_reminder_data



def createReminder(user_id, message:str):
    reminder_data = extract_reminder_data(message)
    print(reminder_data)


    reminder_id = save_reminder(
        user_id,
        reminder_data["product_url"],
        reminder_data["target_price"]
    )

    return { 
        "success": True,
        "message" : "Reminder created succesfully",
        "remidner_id" : reminder_id,
        "data": reminder_data
    } 
 

def updateReminder(user_id, message:str):

    reminders = get_user_reminders(user_id)
    if not reminders:
        return {
            "success": False,
            "message": "You don't have any reminders yet."
        }
    

    response = "Which reminder do you want to update?\n\n"

    sessions[user_id] = {
        "tool": "reminder",
        "action": "update",
        "step": "waiting_for_reminder_selection",
        "status": "waiting_for_input",
        "reminders" : reminders
    }
    
    for index, reminder in enumerate(reminders, start=1):

        response += (
            f"{index}. {reminder['product_url']}\n"
            f"Target Price: ₹{reminder['target_price']}\n\n"
        )

    return {
        "success": True,
        "message": response
    }


def deleteReminder(user_id, message:str):

    reminders = get_user_reminders(user_id)

    if not reminders:
        return {
            "success": False,
            "message": "You don't have any reminders yet."
        }

    response = "Which reminder do you want to delete?\n\n"

    for index, reminder in enumerate(reminders, start=1):

        response += (
            f"{index}. {reminder['product_url']}\n"
            f"Target Price: ₹{reminder['target_price']}\n\n"
        )

    sessions[user_id] = {
        "tool": "reminder",
        "action": "delete",
        "step": "waiting_for_delete_selection",
        "status": "waiting_for_input",
        "reminders": reminders
    }

    return {
        "success": True,
        "message": response
    }


def listReminders(user_id, message):

    reminders = get_user_reminders(
        user_id
    )

    if not reminders:
        return {
            "success": False,
            "message": "You don't have any reminders yet."
        }

    response = "Your reminders:\n\n"

    for reminder in reminders:

        response += (
        f"{reminder['id']}. {reminder['product_url']}\n"
        f"   Target Price: ₹{reminder['target_price']}\n\n"
        )
    return {
        "success": True,
        "message": response
    }



