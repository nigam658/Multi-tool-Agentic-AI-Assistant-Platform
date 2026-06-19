from fastapi import HTTPException

from email_tool.email_service import generate_email_draft, modify_email_draft, detect_email_action, send_email
from session_manager import sessions


def emailAgent(conversation_id : str, message:str):

    session = sessions.get(conversation_id)

    if not session:

        email_draft = generate_email_draft(message)

        # store the draft in the session, we will need it if the user wants to modify, send or cancel the email
        sessions[conversation_id] = {
            "tool": "email",
            "draft": email_draft
        }

        return {
            "success": True,
            "type": "email_draft",
            "draft": email_draft,
            "message": "Please review the draft. You can send, modify, or cancel it. just tell me what you want to do next."
        }
    
    

    action = detect_email_action(message)

    if action not in ["send", "modify", "cancel", "create_new_email"]:
        action = "modify"

    draft = session.get("draft")

    if not draft:
        raise HTTPException(
            status_code = 404,
            detail = "No active email draft found."
        )  
    
    # send email
    if action == "send":
        try:
            send_email(
                recipient=draft["recipient"],
                subject=draft["subject"],
                body=draft["body"]
            )

            del sessions[conversation_id]
            
            return {
                "type": "email_sent",
                "message": "Email sent successfully"
            }
        except Exception as e:
            print(f"Error sending email: {e}")  # for developer logs
            raise HTTPException(
                status_code=500,
                detail="I couldn't send the email."
            )

    # if user wants to cancel the email
    elif action == "cancel":

        del sessions[conversation_id]

        return {
            "type": "email_cancelled",
            "message": "Email cancelled"
        }
    
    # if user wants to modify the email
    elif action == "modify":
        try:
            updated_draft = modify_email_draft(
                draft,
                message
            )

            sessions[conversation_id]["draft"] = updated_draft

            return {
                "type": "updated_draft",
                "updated_draft": updated_draft,
                "message": "Please review the draft. You can send, modify, or cancel it. just tell me what you want to do next."
            }

        except Exception as e:
            print(f"Error modifying draft: {e}")  # for developer logs
            raise HTTPException(
                status_code=500,
                detail="I couldn't update the email. Please try again."
            )

    elif action == "create_new_email":
        try:
            new_draft = generate_email_draft(message)

            sessions[conversation_id]["draft"] = new_draft

            return {
                "type": "email_draft",
                "draft": new_draft,
                "message": "Please review the draft. You can send, modify, or cancel it."
            }

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="I couldn't create the new email draft."
            )

