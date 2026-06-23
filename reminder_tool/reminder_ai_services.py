import json
from ai_client import client

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
