#!/usr/bin/env python3
"""
Test filename sanitization
"""

import sys
sys.path.append('.')

from handlers.message_handler import MessageHandler
from core.database import DatabaseManager
from core.state_manager import StateManager

def test_sanitization():
    """Test the filename sanitization function"""
    # Create a minimal handler instance
    db = None  # We won't use database for this test
    state_manager = None  # We won't use state manager for this test
    handler = MessageHandler(db, state_manager)
    
    # Test problematic filename
    test_filename = "𝐒𝐞𝐬𝐬𝐢𝐨𝐧_𝐓𝐨_𝐭𝐱𝐭_Convert_Done_150.txt"
    
    print(f"Original filename: {test_filename}")
    print(f"Original length: {len(test_filename)}")
    
    sanitized = handler._sanitize_filename(test_filename)
    
    print(f"Sanitized filename: {sanitized}")
    print(f"Sanitized length: {len(sanitized)}")
    
    # Test if sanitized version doesn't cause issues
    try:
        test_message = f"File: {sanitized}"
        test_message.encode('utf-8')
        print("✅ Sanitized filename is safe for Telegram")
    except Exception as e:
        print(f"❌ Sanitized filename still has issues: {e}")

if __name__ == "__main__":
    test_sanitization()
