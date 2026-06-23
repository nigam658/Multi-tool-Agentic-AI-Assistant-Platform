from fastapi import APIRouter
from pydantic import BaseModel

from routers.agent import Agent 
from auth.jwt_handler import verify_token

router = APIRouter()

class ChatRequest(BaseModel):
    token: str
    message: str

@router.post("/chat")
def chat(request:ChatRequest):
    payload = verify_token(
        request.token
    )

    if not payload:
        return {
            "success": False,
            "message": "Unauthorized"
        }
    
    user_id = payload["user_id"]


    response = Agent(user_id, request.message)
    
    return {"response": response}

