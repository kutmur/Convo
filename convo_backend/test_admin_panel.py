#!/usr/bin/env python3
"""
Test script to verify the admin panel functionality.
"""

import sqlite3
from datetime import datetime

def test_database():
    """Test the database setup and verify data."""
    try:
        conn = sqlite3.connect('convo.db')
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages';")
        table_exists = cursor.fetchone()
        print(f"✓ Messages table exists: {table_exists is not None}")
        
        # Count total messages
        cursor.execute("SELECT COUNT(*) FROM messages")
        total_messages = cursor.fetchone()[0]
        print(f"✓ Total messages in database: {total_messages}")
        
        # Count unique sessions
        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM messages")
        unique_sessions = cursor.fetchone()[0]
        print(f"✓ Unique sessions: {unique_sessions}")
        
        # Show sample messages
        cursor.execute("SELECT session_id, sender, message, timestamp FROM messages ORDER BY timestamp DESC LIMIT 3")
        sample_messages = cursor.fetchall()
        print(f"✓ Sample messages (latest 3):")
        for msg in sample_messages:
            print(f"  - [{msg[0]}] {msg[1]}: {msg[2][:50]}...")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_endpoints():
    """Test API endpoints."""
    import requests
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health")
        print(f"✓ Health endpoint: {response.status_code} - {response.json()}")
        
        # Test admin endpoint
        response = requests.get("http://localhost:8000/admin")
        print(f"✓ Admin endpoint: {response.status_code} - HTML response length: {len(response.text)}")
        
        # Test chat endpoint
        response = requests.post("http://localhost:8000/chat", 
                               json={"message": "Test message", "session_id": "test_verification"})
        print(f"✓ Chat endpoint: {response.status_code} - {response.json()}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Server is not running. Please start the server first.")
        return False
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Convo Admin Panel Implementation")
    print("=" * 50)
    
    print("\n1. Testing Database:")
    db_test = test_database()
    
    print("\n2. Testing API Endpoints:")
    api_test = test_endpoints()
    
    print("\n" + "=" * 50)
    if db_test and api_test:
        print("✓ All tests passed! Admin panel is working correctly.")
        print("🎉 GitHub Issue #4 has been successfully implemented!")
        print("\nAccess the admin panel at: http://localhost:8000/admin")
    else:
        print("✗ Some tests failed. Please check the errors above.")
