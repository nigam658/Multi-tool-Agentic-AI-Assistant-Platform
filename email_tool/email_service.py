import json
from ai_client import client

import smtplib
import os
        
def generate_email_draft(message: str):

    prompt = f"""
    You are a professional email assistant.

    Determine the user's intent.

    If the user wants to apply for a job:
    - Write the email as a candidate applying to an employer.

    If the user wants to recruit someone:
    - Write the email as a recruiter contacting a candidate.

    Rules:

    - If the user is applying for a job, write the email as a candidate applying to an employer.
    - If the user is recruiting or approaching someone, write the email as a recruiter or hiring manager.
    - If information is missing, make reasonable assumptions.
    - Create an appropriate subject line.
    - Use a professional tone.
    - Keep the email concise and relevant.
    - Return ONLY valid JSON.
    - Do not include markdown.
    - Do not wrap the response in ```json blocks.
    
    Format:

    {{
        "recipient": "",
        "subject": "",
        "body": "",
        "attachment": ""
    }}

    User Request:
    {message}
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        raw_text = response.text

        raw_text = raw_text.replace("```json","")
        raw_text = raw_text.replace("```","")    
        raw_text = raw_text.strip()

        return json.loads(raw_text)
    
    except Exception as e:
        raise Exception(f"Error in generate_email_draft: {e}")
    

def modify_email_draft(draft, instruction):

    prompt = f"""
    Current Email

    Subject:
    {draft["subject"]}

    Body:
    {draft["body"]}

    User wants:

    {instruction}

    Update the email.

    Return JSON:

    {{
        "recipient":"",
        "subject":"",
        "body":"",
        "attachment":""
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        raw_text = response.text

        raw_text = raw_text.replace("```json", "")
        raw_text = raw_text.replace("```", "")
        raw_text = raw_text.strip()

        return json.loads(raw_text)
    
    except Exception as e:
        raise Exception(f"Error in modify_email_draft: {e}")
    


def detect_email_action(message: str):

    prompt = f"""
    The user is reviewing an email draft.

    Classify the action.

    Possible actions:
    - send
    - modify
    - cancel
    - create_new_email

    
    Rules:
    - If the user wants to edit the current draft, return modify.
    - If the user wants to create a completely new email draft, return create_new_email.
    - If the user wants to send the current draft, return send.
    - If the user wants to discard the current draft, return cancel.

    Return ONLY one word.

    User Message:
    {message}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip().lower()
    
    except Exception as e:
        raise Exception(f"Error in detect_email_action: {e}")


def send_email(recipient,subject,body):

    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("APP_PASSWORD")

    message = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        sender_email,
        sender_password
    )

    server.sendmail(
        sender_email,
        recipient,
        message
    )

    server.quit()

