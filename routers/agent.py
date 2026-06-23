from conservation_tool.chat_service import chatAgent
from email_tool.email_agent import emailAgent
from reminder_tool.reminder_agent import reminderAgent
from session_manager import sessions
from routers.agent_services import detect_tool,detect_workflow_action


TOOLS = {
    "email": emailAgent,
    "reminder": reminderAgent,
    "chat" : chatAgent
} 


def Agent(user_id: int, message: str):

    # Check if user is already inside a tool workflow
    session = sessions.get(user_id)

    if session:
        action = detect_workflow_action(session,message)

        if action == "cancel":

            del sessions[user_id]

            return {
                "success": True,
                "message": "Workflow cancelled."
            }

        if action == "switch":

            del sessions[user_id]

            new_tool = detect_tool(message)
 
            tool = TOOLS.get(new_tool)

            if not tool:
                return {
                    "success": False,
                    "message": "Tool not found."
                }

            return tool(
                user_id,
                message
            )

        return TOOLS[session["tool"]](
            user_id,
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
        user_id,
        message
    )
