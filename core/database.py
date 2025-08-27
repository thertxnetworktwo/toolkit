"""
Database management for RTX Toolkit Bot
"""

import sqlite3
import aiosqlite
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from .config import Config

class DatabaseManager:
    """Database manager with async support"""
    
    def __init__(self, db_path: Path = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / 'data' / 'rtx_toolkit.db'
        
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        
        # Ensure data directory exists
        self.db_path.parent.mkdir(exist_ok=True)
    
    async def initialize(self):
        """Initialize database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Users table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    is_premium BOOLEAN DEFAULT 0,
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Channels table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    channel_id TEXT NOT NULL,
                    channel_name TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Sessions table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    user_id INTEGER PRIMARY KEY,
                    session_data BLOB,
                    phone_number TEXT,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Frozen numbers cache
            await db.execute('''
                CREATE TABLE IF NOT EXISTS frozen_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT,
                    phone_number TEXT,
                    is_frozen BOOLEAN,
                    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(channel_id, phone_number)
                )
            ''')
            
            # Withdraw processing
            await db.execute('''
                CREATE TABLE IF NOT EXISTS withdraw_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    status TEXT DEFAULT 'pending',
                    phone_numbers TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            await db.commit()
            self.logger.info("Database initialized successfully")
    
    # User management
    async def register_user(self, user_id: int, username: str = None, first_name: str = None) -> bool:
        """Register a new user"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'INSERT OR REPLACE INTO users (user_id, username, first_name) VALUES (?, ?, ?)',
                    (user_id, username, first_name)
                )
                await db.commit()
                self.logger.info(f"User {user_id} registered successfully")
                return True
        except Exception as e:
            self.logger.error(f"Failed to register user {user_id}: {e}")
            return False
    
    async def is_user_registered(self, user_id: int) -> bool:
        """Check if user is registered"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
            result = await cursor.fetchone()
            return result is not None
    
    async def update_user_activity(self, user_id: int):
        """Update user's last activity"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE user_id = ?',
                (user_id,)
            )
            await db.commit()
    
    async def set_premium_status(self, user_id: int, is_premium: bool) -> bool:
        """Set user premium status"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'UPDATE users SET is_premium = ? WHERE user_id = ?',
                    (is_premium, user_id)
                )
                await db.commit()
                self.logger.info(f"User {user_id} premium status set to {is_premium}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to update premium status for user {user_id}: {e}")
            return False
    
    async def is_premium_user(self, user_id: int) -> bool:
        """Check if user has premium status (admins automatically have premium)"""
        # Admins automatically have premium access
        config = Config()
        if config.is_admin(user_id):
            return True
            
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT is_premium FROM users WHERE user_id = ?', (user_id,))
            result = await cursor.fetchone()
            return result and result[0] == 1
    
    # Channel management
    async def add_channel(self, user_id: int, channel_id: str, channel_name: str) -> bool:
        """Add a channel for user"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'INSERT INTO channels (user_id, channel_id, channel_name) VALUES (?, ?, ?)',
                    (user_id, channel_id, channel_name)
                )
                await db.commit()
                self.logger.info(f"Channel {channel_id} added for user {user_id}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to add channel for user {user_id}: {e}")
            return False
    
    async def get_user_channels(self, user_id: int) -> List[Dict]:
        """Get all channels for user"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                'SELECT id, channel_id, channel_name, is_active FROM channels WHERE user_id = ? AND is_active = 1',
                (user_id,)
            )
            results = await cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'channel_id': row[1],
                    'channel_name': row[2],
                    'is_active': row[3]
                }
                for row in results
            ]
    
    async def remove_channel(self, user_id: int, channel_db_id: int) -> bool:
        """Remove a channel"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'UPDATE channels SET is_active = 0 WHERE id = ? AND user_id = ?',
                    (channel_db_id, user_id)
                )
                await db.commit()
                return True
        except Exception as e:
            self.logger.error(f"Failed to remove channel {channel_db_id}: {e}")
            return False
    
    # Session management
    async def store_session(self, user_id: int, session_data: bytes, phone_number: str = None) -> bool:
        """Store user session data"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'INSERT OR REPLACE INTO user_sessions (user_id, session_data, phone_number) VALUES (?, ?, ?)',
                    (user_id, session_data, phone_number)
                )
                await db.commit()
                self.logger.info(f"Session stored for user {user_id}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to store session for user {user_id}: {e}")
            return False
    
    async def get_session(self, user_id: int) -> Optional[bytes]:
        """Get user session data"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                'SELECT session_data FROM user_sessions WHERE user_id = ? AND is_active = 1',
                (user_id,)
            )
            result = await cursor.fetchone()
            return result[0] if result else None
    
    async def has_session(self, user_id: int) -> bool:
        """Check if user has an active session"""
        session = await self.get_session(user_id)
        return session is not None
    
    async def get_user_session(self, user_id: int) -> Optional[dict]:
        """Get user session information"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute(
                    'SELECT session_data, phone_number, created_at FROM user_sessions WHERE user_id = ? AND is_active = 1',
                    (user_id,)
                ) as cursor:
                    result = await cursor.fetchone()
                    if result:
                        return {
                            'session_data': result[0],
                            'phone_number': result[1],
                            'created_at': result[2]
                        }
                    return None
        except Exception as e:
            self.logger.error(f"Failed to get user session for {user_id}: {e}")
            return None
    
    async def remove_user_session(self, user_id: int) -> bool:
        """Remove user session"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'UPDATE user_sessions SET is_active = 0 WHERE user_id = ?',
                    (user_id,)
                )
                await db.commit()
                self.logger.info(f"Session removed for user {user_id}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to remove session for user {user_id}: {e}")
            return False
    
    # Frozen cache management
    async def cache_frozen_result(self, channel_id: str, phone_number: str, is_frozen: bool):
        """Cache frozen check result"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT OR REPLACE INTO frozen_cache (channel_id, phone_number, is_frozen) VALUES (?, ?, ?)',
                (channel_id, phone_number, is_frozen)
            )
            await db.commit()
    
    async def get_cached_result(self, channel_id: str, phone_number: str) -> Optional[bool]:
        """Get cached frozen result if recent"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                '''SELECT is_frozen FROM frozen_cache 
                   WHERE channel_id = ? AND phone_number = ? 
                   AND datetime(checked_at) > datetime('now', '-1 hour')''',
                (channel_id, phone_number)
            )
            result = await cursor.fetchone()
            return result[0] if result else None
    
    async def close(self):
        """Close database connections"""
        # For aiosqlite, connections are automatically closed
        self.logger.info("Database connections closed")
