"""
Command handlers for bot commands
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.database import DatabaseManager
from core.state_manager import StateManager, UserState

class CommandHandler:
    """Handles bot commands"""
    
    def __init__(self, db: DatabaseManager, state_manager: StateManager):
        self.db = db
        self.state_manager = state_manager
        self.logger = logging.getLogger(__name__)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - Main menu"""
        user = update.effective_user
        user_id = user.id
        
        # Update user activity
        await self.db.update_user_activity(user_id)
        
        # Clear any existing state
        self.state_manager.clear_state(user_id)
        
        # Check if user is registered
        if not await self.db.is_user_registered(user_id):
            # Register new user
            await self.db.register_user(user_id, user.username, user.first_name)
            
            welcome_message = f"""
🤖 **Welcome to RTX Toolkit Bot!**

👋 Hi {user.first_name}! I'm your professional Telegram numbers checker.

🚀 **Get Started:**
• Upload your session file to begin
• Add channels to monitor
• Check frozen numbers efficiently

Choose an option below:
            """
        else:
            # Existing user - show dashboard
            is_premium = await self.db.is_premium_user(user_id)
            has_session = await self.db.has_session(user_id)
            channels = await self.db.get_user_channels(user_id)
            
            status_emoji = "⭐" if is_premium else "🆓"
            status_text = "Premium" if is_premium else "Free"
            session_emoji = "✅" if has_session else "🔄"
            
            welcome_message = f"""
🤖 **RTX Toolkit Dashboard**

👋 Welcome back, {user.first_name}!

📊 **Your Stats:**
• Status: {status_emoji} {status_text}
• Session: {session_emoji} {'Connected' if has_session else 'Required'}
• Channels: {len(channels)}

🚀 **Quick Actions:**
            """
        
        # Build menu based on user status
        keyboard = await self._build_main_menu(user_id)
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **RTX Toolkit Bot Help**

**📋 Main Features:**
• ❄️ Check frozen Telegram numbers
• 📂 Manage multiple channels
• 💰 Process withdraw requests
• 🔐 Session management

**🎯 How to Use:**
1. Upload your Telegram session file
2. Add channels you want to monitor
3. Use the check frozen feature
4. Process withdraw requests

**⭐ Premium Features:**
• Unlimited channels
• Priority processing
• Advanced analytics
• Bulk operations

**🆘 Need Help?**
Contact support or use the menu buttons for easy navigation.
        """
        
        keyboard = [
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')],
            [InlineKeyboardButton("⭐ Get Premium", callback_data='premium_info')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            help_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        user_id = update.effective_user.id
        
        if not await self.db.is_user_registered(user_id):
            await update.message.reply_text("Please start the bot first using /start")
            return
        
        # Get user info
        is_premium = await self.db.is_premium_user(user_id)
        has_session = await self.db.has_session(user_id)
        channels = await self.db.get_user_channels(user_id)
        current_state = self.state_manager.get_state(user_id)
        
        status_text = f"""
📊 **Your Status**

👤 **Account:**
• Premium: {'✅ Yes' if is_premium else '🔄 No'}
• Session: {'✅ Connected' if has_session else '🔄 Required'}

📂 **Channels:** {len(channels)}
        """
        
        if channels:
            status_text += "\n🔹 " + "\n🔹 ".join([f"{ch['channel_name']}" for ch in channels[:5]])
            if len(channels) > 5:
                status_text += f"\n... and {len(channels) - 5} more"
        
        status_text += f"\n\n🤖 **Bot State:** {current_state.value.title()}"
        
        keyboard = [
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')],
            [InlineKeyboardButton("📂 Manage Channels", callback_data='manage_channels')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            status_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /admin command"""
        user_id = update.effective_user.id
        
        # Check if user is admin (we'll need to import config)
        from core.config import Config
        config = Config()
        
        if not config.is_admin(user_id):
            await update.message.reply_text("🔄 Access denied. Admin only.")
            return
        
        admin_text = """
🔧 **Admin Panel**

👥 **User Management:**
• Add/Remove premium users
• View user statistics
• Manage user sessions

📊 **System Status:**
• Monitor bot performance
• Check database health
• View error logs

⚙️ **Configuration:**
• Update bot settings
• Manage features
        """
        
        keyboard = [
            [
                InlineKeyboardButton("👥 User Management", callback_data='admin_users'),
                InlineKeyboardButton("📊 Statistics", callback_data='admin_stats')
            ],
            [
                InlineKeyboardButton("⚙️ Settings", callback_data='admin_settings'),
                InlineKeyboardButton("📝 Logs", callback_data='admin_logs')
            ],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            admin_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def _build_main_menu(self, user_id: int) -> list:
        """Build main menu based on user status"""
        is_premium = await self.db.is_premium_user(user_id)
        has_session = await self.db.has_session(user_id)
        channels = await self.db.get_user_channels(user_id)
        
        keyboard = []
        
        if is_premium and has_session and channels:
            # Full access menu
            keyboard = [
                [
                    InlineKeyboardButton("❄️ Check Frozen", callback_data='check_frozen'),
                    InlineKeyboardButton("💰 Process Withdraw", callback_data='process_bulk_withdraw')
                ],
                [
                    InlineKeyboardButton("📂 Channels", callback_data='manage_channels'),
                    InlineKeyboardButton("🔐 Session", callback_data='session_menu')
                ],
                [
                    InlineKeyboardButton("📊 Status", callback_data='view_status'),
                    InlineKeyboardButton("❓ Help", callback_data='help')
                ]
            ]
        elif is_premium and has_session:
            # Need to add channels
            keyboard = [
                [InlineKeyboardButton("📂 Add Channels First", callback_data='manage_channels')],
                [
                    InlineKeyboardButton("🔐 Session", callback_data='session_menu'),
                    InlineKeyboardButton("📊 Status", callback_data='view_status')
                ],
                [InlineKeyboardButton("❓ Help", callback_data='help')]
            ]
        elif is_premium:
            # Need session
            keyboard = [
                [InlineKeyboardButton("🔐 Upload Session First", callback_data='session_menu')],
                [
                    InlineKeyboardButton("📊 Status", callback_data='view_status'),
                    InlineKeyboardButton("❓ Help", callback_data='help')
                ]
            ]
        else:
            # Need premium
            keyboard = [
                [InlineKeyboardButton("⭐ Get Premium Access", callback_data='premium_info')],
                [
                    InlineKeyboardButton("📊 Status", callback_data='view_status'),
                    InlineKeyboardButton("❓ Help", callback_data='help')
                ]
            ]
        
        return keyboard
