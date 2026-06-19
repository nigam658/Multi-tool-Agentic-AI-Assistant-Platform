import json

from conservation_tool.chat_service import chatAgent
from email_tool.email_agent import emailAgent
from reminder_tool.reminder_agent import reminderAgent
from session_manager import sessions
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

TOOLS = {
    "email": emailAgent,
    "reminder": reminderAgent,
    "chat" : chatAgent
} 


def Agent(conversation_id: str, message: str):

    # Check if user is already inside a tool workflow
    session = sessions.get(conversation_id)

    if session:
        if session.get("status") == "waiting_for_input":

            return TOOLS[session["tool"]](
                conversation_id,
                message
            )
        
        current_tool = session["tool"]

        new_tool = detect_tool(message)

        if new_tool and new_tool != current_tool:

            del sessions[conversation_id]

            return TOOLS[new_tool](
                conversation_id,
                message
            )
        
        return TOOLS[current_tool](
                conversation_id,
                message
            )


    # No active workflow, ask LLM which tool should handle this
    tool_name = detect_tool(message)

    tool = TOOLS.get(tool_name)

    if not tool:
        return {
            "success": False,
            "message": "something went wrong."
        }

    return tool(
        conversation_id,
        message
    )
