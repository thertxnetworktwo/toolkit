"""
State management for user interactions
"""

from enum import Enum
from typing import Dict, Optional, Any
import logging

class UserState(Enum):
    """User interaction states"""
    IDLE = "idle"
    CHANNEL_SETUP = "channel_setup"
    CHANNEL_EDIT = "channel_edit"
    SESSION_UPLOAD = "session_upload"
    WITHDRAW_PROCESSING = "withdraw_processing"
    ADMIN_COMMAND = "admin_command"
    FILE_UPLOAD = "file_upload"

class StateManager:
    """Manages user states and context data"""
    
    def __init__(self):
        self.user_states: Dict[int, UserState] = {}
        self.user_contexts: Dict[int, Dict[str, Any]] = {}
        self.logger = logging.getLogger(__name__)
    
    def set_state(self, user_id: int, state: UserState, context: Optional[Dict[str, Any]] = None):
        """Set user state with optional context"""
        self.user_states[user_id] = state
        
        if context:
            if user_id not in self.user_contexts:
                self.user_contexts[user_id] = {}
            self.user_contexts[user_id].update(context)
        
        self.logger.debug(f"User {user_id} state changed to {state.value}")
    
    def get_state(self, user_id: int) -> UserState:
        """Get current user state"""
        return self.user_states.get(user_id, UserState.IDLE)
    
    def clear_state(self, user_id: int):
        """Clear user state and context"""
        self.user_states.pop(user_id, None)
        self.user_contexts.pop(user_id, None)
        self.logger.debug(f"User {user_id} state cleared")
    
    def get_context(self, user_id: int, key: str = None) -> Any:
        """Get user context data"""
        if user_id not in self.user_contexts:
            return None
        
        if key:
            return self.user_contexts[user_id].get(key)
        
        return self.user_contexts[user_id]
    
    def set_context(self, user_id: int, key: str, value: Any):
        """Set user context data"""
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = {}
        
        self.user_contexts[user_id][key] = value
        self.logger.debug(f"User {user_id} context updated: {key}")
    
    def clear_context(self, user_id: int, key: str = None):
        """Clear specific context key or all context"""
        if user_id not in self.user_contexts:
            return
        
        if key:
            self.user_contexts[user_id].pop(key, None)
        else:
            self.user_contexts[user_id].clear()
    
    def is_state(self, user_id: int, state: UserState) -> bool:
        """Check if user is in specific state"""
        return self.get_state(user_id) == state
