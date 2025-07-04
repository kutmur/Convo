# Convo Admin Panel - Setup Instructions

This document provides complete setup instructions for the admin panel feature implemented for GitHub Issue #4.

## Overview

The admin panel provides a web-based interface to view chat messages and basic statistics for the Convo chatbot platform. It includes:

- **Statistics Dashboard**: Total messages, chat sessions, user messages, and bot messages
- **Message History**: Complete chat history with session IDs, timestamps, senders, and messages
- **Modern UI**: Clean, responsive design with professional styling

## Files Created/Modified

### Backend Files

1. **`convo_backend/main.py`** - Updated with:
   - New `/admin` endpoint
   - Database initialization functions
   - Message storage and retrieval functions
   - Statistics calculation functions
   - Updated chat endpoint to save messages to database

2. **`convo_backend/requirements.txt`** - Added:
   - `jinja2==3.1.2` (for HTML templating)
   - `aiosqlite==0.19.0` (for async SQLite database operations)

3. **`convo_backend/seed_database.py`** - New file:
   - Script to create sample data for testing
   - Generates realistic chat conversations with multiple sessions

### Frontend Files

4. **`convo_backend/templates/admin.html`** - New file:
   - Complete HTML template with embedded CSS
   - Responsive design with modern styling
   - Statistics cards and message table
   - Jinja2 template integration

5. **`convo_backend/templates/` directory** - New directory for HTML templates

## Setup Instructions

### Step 1: Install Dependencies

Navigate to the backend directory and install the required packages:

```bash
cd convo_backend
pip install -r requirements.txt
```

### Step 2: Create Sample Data (Optional)

To test the admin panel with sample data:

```bash
cd convo_backend
python seed_database.py
```

This will create a `convo.db` file with sample chat conversations.

### Step 3: Start the Server

```bash
cd convo_backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 4: Access the Admin Panel

Open your web browser and navigate to:
```
http://localhost:8000/admin
```

## API Endpoints

### New Admin Endpoint

- **GET `/admin`**: Returns the admin panel HTML page with message statistics and chat history

### Updated Chat Endpoint

- **POST `/chat`**: Now saves both user messages and bot responses to the database
  - Request body: `{"message": "your message", "session_id": "optional_session_id"}`
  - If no session_id is provided, "default" is used

## Database Schema

The SQLite database (`convo.db`) contains a single table:

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    sender TEXT NOT NULL,         -- 'user' or 'bot'
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Features

### Statistics Dashboard
- Total number of messages
- Number of unique chat sessions
- Breakdown of user vs bot messages
- Visual cards with hover effects

### Message History
- Recent 100 messages displayed in reverse chronological order
- Session ID tracking
- Timestamp formatting
- Sender identification with colored badges
- Responsive table design

### Error Handling
- Database connection error handling
- Graceful fallback when no messages exist
- Timestamp parsing error handling

## Docker Support

The admin panel is fully compatible with the existing Docker setup. The `Dockerfile` already includes all necessary dependencies and will automatically serve the admin panel when the container is running.

## Security Note

**Important**: This admin panel currently has no authentication. In a production environment, you should add proper authentication and authorization before deploying.

## Testing the Feature

1. Start the server using the instructions above
2. Send some chat messages to the `/chat` endpoint:
   ```bash
   curl -X POST "http://localhost:8000/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello!", "session_id": "test_session"}'
   ```
3. Visit the admin panel at `http://localhost:8000/admin` to see the messages

## Troubleshooting

### Database Issues
- If you encounter database errors, delete the `convo.db` file and restart the server
- The database will be automatically recreated on startup

### Template Not Found
- Ensure the `templates` directory exists in the `convo_backend` folder
- Verify that `admin.html` is in the `templates` directory

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're running the commands from the correct directory

## Project Structure After Implementation

```
convo_backend/
├── templates/
│   └── admin.html          # Admin panel HTML template
├── Dockerfile              # Container configuration
├── main.py                 # Updated FastAPI application
├── requirements.txt        # Updated dependencies
├── seed_database.py        # Sample data generator
└── convo.db               # SQLite database (created automatically)
```

This implementation fully satisfies the requirements of GitHub Issue #4 by providing a basic admin panel to view past chats and basic statistics, with no authentication required as specified.
