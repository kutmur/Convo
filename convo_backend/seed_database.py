#!/usr/bin/env python3
"""
Database seeder script for Convo admin panel testing.
This script creates sample data to demonstrate the admin panel functionality.
"""

import sqlite3
from datetime import datetime, timedelta
import random

# Sample messages for testing
sample_conversations = [
    {
        "session_id": "session_001",
        "messages": [
            ("user", "Hello, how are you?"),
            ("bot", "Hello! I'm doing well, thank you for asking. How can I help you today?"),
            ("user", "I need help with my account"),
            ("bot", "I'd be happy to help you with your account. What specific issue are you experiencing?"),
            ("user", "I can't remember my password"),
            ("bot", "I can help you reset your password. Please check your email for reset instructions."),
        ]
    },
    {
        "session_id": "session_002",
        "messages": [
            ("user", "What's the weather like today?"),
            ("bot", "I don't have access to current weather data, but I can help you with other questions!"),
            ("user", "Can you tell me a joke?"),
            ("bot", "Sure! Why don't scientists trust atoms? Because they make up everything!"),
            ("user", "That's funny!"),
            ("bot", "I'm glad you enjoyed it! Is there anything else I can help you with?"),
        ]
    },
    {
        "session_id": "session_003",
        "messages": [
            ("user", "I need technical support"),
            ("bot", "I'm here to help with technical issues. What problem are you experiencing?"),
            ("user", "My application keeps crashing"),
            ("bot", "I understand how frustrating that can be. Can you tell me what happens just before it crashes?"),
            ("user", "It happens when I try to save a file"),
            ("bot", "This could be a permissions issue. Have you tried running the application as administrator?"),
            ("user", "Let me try that"),
            ("bot", "Great! Let me know if that resolves the issue or if you need further assistance."),
        ]
    },
    {
        "session_id": "session_004",
        "messages": [
            ("user", "Hi there!"),
            ("bot", "Hello! Welcome to Convo. How can I assist you today?"),
            ("user", "I'm just testing the system"),
            ("bot", "Perfect! Feel free to ask me anything. I'm here to help and learn from our conversation."),
        ]
    },
    {
        "session_id": "session_005",
        "messages": [
            ("user", "What can you do?"),
            ("bot", "I can help answer questions, provide information, and have conversations with you. What would you like to know?"),
            ("user", "That's impressive"),
            ("bot", "Thank you! I'm designed to be helpful and engaging. Is there a particular topic you'd like to discuss?"),
        ]
    }
]

def create_sample_database():
    """Create a sample database with test data."""
    conn = sqlite3.connect('convo.db')
    cursor = conn.cursor()
    
    # Create the messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Clear existing data
    cursor.execute('DELETE FROM messages')
    
    # Insert sample data
    base_time = datetime.now() - timedelta(days=7)  # Start from 7 days ago
    
    for i, conversation in enumerate(sample_conversations):
        session_id = conversation["session_id"]
        session_start = base_time + timedelta(days=i, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        for j, (sender, message) in enumerate(conversation["messages"]):
            # Add some time between messages (1-5 minutes)
            message_time = session_start + timedelta(minutes=j * random.randint(1, 5))
            
            cursor.execute('''
                INSERT INTO messages (session_id, sender, message, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (session_id, sender, message, message_time.isoformat()))
    
    conn.commit()
    conn.close()
    print("Sample database created successfully!")
    print("You can now access the admin panel at: http://localhost:8000/admin")

if __name__ == "__main__":
    create_sample_database()
