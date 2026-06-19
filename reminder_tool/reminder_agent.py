from session_manager import sessions
from reminder_tool.reminder_service import (detect_reminder_action, createReminder, updateReminder, deleteReminder, listReminders)
from reminder_tool.reminder_repository import update_reminder_price, delete_reminder

ACTIONS = {
    "create": createReminder,
    "update": updateReminder,
    "delete": deleteReminder,
    "list": listReminders
}

def reminderAgent(conversation_id: str, message: str):

    session = sessions.get(conversation_id)

    if session:

        if session["step"] == "waiting_for_reminder_selection":

            try:
                choice = int(message)

            except ValueError:

                return {
                    "success": False,
                    "message": "Please enter a valid reminder number."
                }

            reminders = session["reminders"]

            if choice < 1 or choice > len(reminders):

                return {
                    "success": False,
                    "message": "Please choose a valid reminder number."
                }

            selected_reminder = reminders[choice - 1]

            sessions[conversation_id]["reminder_id"] = selected_reminder["id"]

            sessions[conversation_id]["step"] = "waiting_for_new_price"

            return {
                "success": True,
                "message": "What is the new target price?"
            }
        
        if session["step"] == "waiting_for_new_price":

            try:
                new_price = float(message)
                if new_price <= 0:
                    return {
                        "success": False,
                        "message": "Price must be greater than 0."
                    }

            except ValueError:

                return {
                    "success": False,
                    "message": "Please enter a valid price."
                }

            sessions[conversation_id]["new_price"] = new_price

            sessions[conversation_id]["step"] = "waiting_for_confirmation"

            return {
                "success": True,
                "message": (
                    f"Please confirm:\n"
                    f"Reminder ID: {session['reminder_id']}\n"
                    f"New Price: ₹{new_price}\n\n"
                    f"Reply with yes or no."
                )
            }
        
        if session["step"] == "waiting_for_confirmation":
            answer = message.lower().strip()

            if answer == "yes":

                try:

                    reminder_id = session.get("reminder_id")

                    new_price = session.get("new_price")

                    update_reminder_price(
                        reminder_id,
                        new_price
                    )

                    del sessions[conversation_id]

                    return {
                        "success": True,
                        "message": "Reminder updated successfully."
                    }

                except Exception as e:
                    print("Update Error:", e)
                    return {
                        "success": False,
                        "message": "Failed to update reminder."
                    }

            if answer == "no":

                del sessions[conversation_id]

                return {
                    "success": True,
                    "message": "Update cancelled."
                }

            return {
                "success": False,
                "message": "Please reply with yes or no."
            }
        

        if session["step"] == "waiting_for_delete_selection":
            try:
                choice = int(message)

            except ValueError:

                return {
                    "success": False,
                    "message": "Please enter a valid reminder number."
                }

            reminders = session["reminders"]

            if choice < 1 or choice > len(reminders):

                return {
                    "success": False,
                    "message": "Please choose a valid reminder number."
                }

            selected_reminder = reminders[choice - 1]

            sessions[conversation_id]["reminder_id"] = selected_reminder["id"]

            sessions[conversation_id]["step"] = "waiting_for_delete_confirmation"

            return {
                "success": True,
                "message": (
                    f"Are you sure you want to delete:\n"
                    f"{selected_reminder['product_url']}?\n\n"
                    f"Reply with yes or no."
                )
            }
        
        if session["step"] == "waiting_for_delete_confirmation":
            answer = message.lower().strip()

            if answer == "yes":

                try:

                    delete_reminder(
                        session["reminder_id"]
                    )

                    del sessions[conversation_id]

                    return {
                        "success": True,
                        "message": "Reminder deleted successfully."
                    }

                except Exception as e:

                    print("Delete Error:", e)

                    return {
                        "success": False,
                        "message": "Failed to delete reminder."
                    }

            if answer == "no":

                del sessions[conversation_id]

                return {
                    "success": True,
                    "message": "Deletion cancelled."
                }

            return {
                "success": False,
                "message": "Please reply with yes or no."
            }

    action = detect_reminder_action(message)

    if action not in ACTIONS:
        return {
            "success": False,
            "message": "I couldn't understand your reminder request."
        }

    return ACTIONS[action](
    conversation_id,
    message
    )