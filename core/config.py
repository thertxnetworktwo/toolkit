"""
Configuration management for RTX Toolkit Bot
"""

import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    """Configuration class for bot settings"""
    
    def __init__(self):
        # Load environment variables
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(env_path)
        
        # Bot configuration
        self.bot_token = os.getenv('BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("BOT_TOKEN not found in environment variables")
        
        # Telegram API configuration
        self.api_id = os.getenv('API_ID')
        self.api_hash = os.getenv('API_HASH')
        
        # Admin configuration
        admin_ids = os.getenv('ADMIN_IDS', '')
        self.admin_ids = [int(id.strip()) for id in admin_ids.split(',') if id.strip().isdigit()]
        
        # Database configuration
        self.db_path = Path(__file__).parent.parent / 'data' / 'rtx_toolkit.db'
        
        # Logging configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = Path(__file__).parent.parent / 'data' / 'bot.log'
        
        # Features configuration
        self.max_channels_free = 5
        self.max_channels_premium = 100
        self.session_timeout = 3600  # 1 hour
        
        # Validate required settings
        self._validate()
    
    def _validate(self):
        """Validate required configuration"""
        if not self.bot_token:
            raise ValueError("BOT_TOKEN is required")
        
        if not self.admin_ids:
            raise ValueError("At least one ADMIN_ID is required")
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is an admin"""
        return user_id in self.admin_ids
