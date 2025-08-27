#!/usr/bin/env python3
"""
Icon replacement script to make the bot interface more professional
"""

import os
import re

# Icon mapping for better UX
ICON_REPLACEMENTS = {
    # Error states - use warning/info instead of harsh X
    "❌ **Invalid Format**": "⚠️ **Invalid Format**",
    "❌ **Invalid File Type**": "⚠️ **Invalid File Type**", 
    "❌ **Channel Limit Reached**": "⚠️ **Channel Limit Reached**",
    "❌ **Session Status:** Not Connected": "🔄 **Session Status:** Not Connected",
    
    # Buttons - use more friendly icons
    "❌ Cancel": "🔙 Cancel",
    "❌ Remove": "🗑️ Remove",
    "❌ Close": "🔙 Close",
    "❌ Remove Session": "🗑️ Remove Session",
    
    # Status indicators - softer approach
    "❌ Inactive": "🔄 Inactive", 
    "❌ Required": "🔄 Required",
    "❌": "🔄",  # Generic status replacement
    
    # Error messages - use warning icon
    "❌ Unknown action": "⚠️ Unknown action",
    "❌ Access denied": "🔒 Access denied", 
    "❌ Failed to": "⚠️ Failed to",
    "❌ Error": "⚠️ Error",
    "❌ Could not": "⚠️ Could not",
    "❌ Invalid": "⚠️ Invalid",
    "❌ No": "ℹ️ No",  # Informational rather than error
}

def replace_icons_in_file(file_path):
    """Replace icons in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for old_icon, new_icon in ICON_REPLACEMENTS.items():
            content = content.replace(old_icon, new_icon)
        
        # Save if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated icons in: {file_path}")
            return True
        else:
            print(f"ℹ️ No changes needed in: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Replace icons in all handler files"""
    handler_files = [
        'handlers/callback_handler.py',
        'handlers/command_handler.py', 
        'handlers/message_handler.py'
    ]
    
    total_updated = 0
    
    for file_path in handler_files:
        if os.path.exists(file_path):
            if replace_icons_in_file(file_path):
                total_updated += 1
        else:
            print(f"⚠️ File not found: {file_path}")
    
    print(f"\n🎉 Icon replacement complete! Updated {total_updated} files.")
    print("The bot interface now uses more professional and friendly icons! 🚀")

if __name__ == "__main__":
    main()
