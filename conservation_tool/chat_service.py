from ai_client import client

def chatAgent(conversation_id,message):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=message
    )

    return {
        "success": True,
        "message": response.text
    }