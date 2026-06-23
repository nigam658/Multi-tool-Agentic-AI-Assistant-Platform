import json
from ai_client import client

def detect_tool(message: str):

    prompt = f"""
    You are a tool router.

    Available tools:

    email
    - Send emails
    - Modify emails
    - Cancel emails

    reminder
    - Set reminders
    - Modify reminders
    - Cancel reminders

    chat
    - Engage in conversation
    - Greetings
    - Questions and answers


    Return ONLY JSON.

    User: Send an email to hr@company.com
    {{"tool":"email"}}

    User: Notify me when this product goes below ₹500
    {{"tool":"reminder"}}

    User: Hello
    {{"tool":"chat"}}

    User: What is Python?
    {{"tool":"chat"}}


    User Message:
    {message}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        result = json.loads(response.text)

        tool = result.get("tool")

        if tool not in ["email", "reminder", "chat"]:
            return "chat"

        return tool

    except Exception:
        return "chat"


def detect_workflow_action(session: dict, message: str):

    prompt = f"""
    You are a workflow controller.

    Current Tool:
    {session.get("tool")}

    Current Step:
    {session.get("step")}

    User Message:
    {message}

    Decide whether the user wants to:

    1. continue
       - Answering the current question
       - Providing requested information

    2. switch
       - Starting a different task
       - Using a different tool

    3. cancel
       - Cancel current workflow
       - Stop current operation

    Examples:

    Current Tool: reminder
    Current Step: waiting_for_new_price
    User Message: 500

    {{"action":"continue"}}

    Current Tool: reminder
    Current Step: waiting_for_new_price
    User Message: Send an email to HR

    {{"action":"switch"}}

    Current Tool: reminder
    Current Step: waiting_for_new_price
    User Message: cancel this

    {{"action":"cancel"}}

    Return ONLY JSON.

    Format:

    {{"action":"continue"}}

    or

    {{"action":"switch"}}

    or

    {{"action":"cancel"}}
    """

    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        result = json.loads(response.text)

        action = result.get("action")

        if action not in ["continue", "switch", "cancel"]:
            return "continue"

        return action

    except Exception:
        return "continue"