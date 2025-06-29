# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    # Simple test case - remove this later
    if request.message.lower() == "hello":
        return {"reply": "hello"}
    
    return {"reply": f"This is a dummy response to your message: '{request.message}'"} 