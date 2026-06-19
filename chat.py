from fastapi import FastAPI
from pydantic import BaseModel

from agent import Agent 


app = FastAPI()

class ChatRequest(BaseModel):
    conversation_id: str
    message: str

@app.post("/chat")
def chat(request:ChatRequest):
    response = Agent(request.conversation_id, request.message)
    
    return {"response": response}

