# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import aiosqlite
import asyncio
from datetime import datetime
from typing import List, Dict, Any
import os

app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Database configuration
DATABASE_PATH = "convo.db"

# Database initialization
async def init_database():
    """Initialize the database and create the messages table if it doesn't exist."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

# Database helper functions
async def get_all_messages() -> List[Dict[str, Any]]:
    """Fetch all messages from the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('''
            SELECT id, session_id, sender, message, timestamp 
            FROM messages 
            ORDER BY timestamp DESC 
            LIMIT 100
        ''') as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def get_message_stats() -> Dict[str, int]:
    """Get basic statistics about messages."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Total messages
        async with db.execute('SELECT COUNT(*) FROM messages') as cursor:
            total_messages = (await cursor.fetchone())[0]
        
        # Total unique sessions
        async with db.execute('SELECT COUNT(DISTINCT session_id) FROM messages') as cursor:
            total_sessions = (await cursor.fetchone())[0]
        
        # User messages
        async with db.execute('SELECT COUNT(*) FROM messages WHERE sender = "user"') as cursor:
            user_messages = (await cursor.fetchone())[0]
        
        # Bot messages
        async with db.execute('SELECT COUNT(*) FROM messages WHERE sender = "bot"') as cursor:
            bot_messages = (await cursor.fetchone())[0]
        
        return {
            'total_messages': total_messages,
            'total_sessions': total_sessions,
            'user_messages': user_messages,
            'bot_messages': bot_messages
        }

async def save_message(session_id: str, sender: str, message: str):
    """Save a message to the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            INSERT INTO messages (session_id, sender, message, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (session_id, sender, message, datetime.now().isoformat()))
        await db.commit()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    await init_database()

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
    session_id: str = "default"

# Root endpoint - provide info about available endpoints
@app.get("/")
async def root():
    """
    Root endpoint that provides information about available endpoints.
    """
    return {
        "message": "Welcome to Convo API",
        "version": "1.0.0",
        "description": "Open-source, self-hostable chatbot platform",
        "endpoints": {
            "admin_panel": "/admin - View chat messages and statistics",
            "health_check": "/health - API health status",
            "chat": "/chat (POST) - Send chat messages",
            "documentation": "/docs - FastAPI documentation"
        },
        "quick_links": {
            "admin_panel": "http://localhost:8000/admin",
            "api_docs": "http://localhost:8000/docs"
        }
    }

# Admin endpoint
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    """
    Admin panel endpoint that displays all chat messages and basic statistics.
    """
    try:
        # Get all messages and statistics
        messages = await get_all_messages()
        stats = await get_message_stats()
        
        # Format timestamps for better display
        for message in messages:
            if message['timestamp']:
                # Parse the timestamp and format it nicely
                try:
                    dt = datetime.fromisoformat(message['timestamp'].replace('Z', '+00:00'))
                    message['timestamp'] = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    # If parsing fails, keep the original timestamp
                    pass
        
        return templates.TemplateResponse("admin.html", {
            "request": request,
            "messages": messages,
            "total_messages": stats['total_messages'],
            "total_sessions": stats['total_sessions'],
            "user_messages": stats['user_messages'],
            "bot_messages": stats['bot_messages']
        })
    except Exception as e:
        # In case of database errors, return a basic error page
        return templates.TemplateResponse("admin.html", {
            "request": request,
            "messages": [],
            "total_messages": 0,
            "total_sessions": 0,
            "user_messages": 0,
            "bot_messages": 0,
            "error": str(e)
        })

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
    # Save the user message to the database
    await save_message(request.session_id, "user", request.message)
    
    # Simple test case - remove this later
    if request.message.lower() == "hello":
        response_message = "Hello! How can I help you today?"
    else:
        response_message = f"This is a dummy response to your message: '{request.message}'"
    
    # Save the bot response to the database
    await save_message(request.session_id, "bot", response_message)
    
    return {"reply": response_message}