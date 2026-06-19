import json
from ai_client import client

from reminder_tool.reminder_repository import save_reminder, get_user_reminders
from session_manager import sessions

def extract_reminder_data(message: str):

    prompt = f"""
    You are a reminder extraction agent.

    Extract:

    - product_url
    - target_price

   Return ONLY valid JSON.

    Do not use markdown.
    Do not use ```json.
    Do not explain.

    Schema:

    {{
    "product_url": string | null,
    "target_price": number | null
    }}

    User:
    {message}
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print("RAW RESPONSE:")
        print(response.text)

        return json.loads(response.text)

    except Exception as e:

        return {
            "product_url": None,
            "target_price": None,
            "error": str(e)
        }

def detect_reminder_action(message: str):

    prompt = f"""
    You are a reminder action router.

    Actions:

    create
    - create reminder
    - notify me
    - track product

    update
    - change reminder
    - update reminder
    - modify alert

    delete
    - delete reminder
    - cancel reminder
    - remove alert

    list
    - show reminders
    - my wishlist
    - active reminders

    Return JSON only.

    User: notify me below 500
    {{"action":"create"}}

    User: change my reminder
    {{"action":"update"}}

    User: delete my reminder
    {{"action":"delete"}}

    User: show my reminders
    {{"action":"list"}}

    User:
    {message}
    """

    response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

    result = json.loads(response.text)

    action = result.get("action")

    return action


def createReminder(conversation_id, message:str):
    reminder_data = extract_reminder_data(message)
    print(reminder_data)


    reminder_id = save_reminder(
        conversation_id,
        reminder_data["product_url"],
        reminder_data["target_price"]
    )

    return {
        "success": True,
        "message" : "Reminder created succesfully",
        "remidner_id" : reminder_id,
        "data": reminder_data
    } 
 

def updateReminder(conversation_id, message:str):

    reminders = get_user_reminders(conversation_id)
    if not reminders:
        return {
            "success": False,
            "message": "You don't have any reminders yet."
        }
    

    response = "Which reminder do you want to update?\n\n"

    sessions[conversation_id] = {
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


def deleteReminder(conversation_id, message:str):

    reminders = get_user_reminders(conversation_id)

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

    sessions[conversation_id] = {
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


def listReminders(conversation_id, message):

    reminders = get_user_reminders(
        conversation_id
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



