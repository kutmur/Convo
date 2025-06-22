# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Pydantic model for the request body of the /chat endpoint
class ChatRequest(BaseModel):
    message: str

# GET endpoint for health checks
@app.get("/health")
async def health_check():
    """
    This endpoint can be used for health checks.
    It returns a simple JSON response indicating the service is running.
    """
    return {"status": "OK"}

# POST endpoint to handle chat messages
@app.post("/chat")
async def chat(request: ChatRequest):
    """
    This endpoint receives a chat message and returns a dummy response.
    It uses the ChatRequest model for request body validation.
    """
    return {"reply": f"This is a dummy response to your message: '{request.message}'"} 