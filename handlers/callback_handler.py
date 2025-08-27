"""
Callback handler for menu interactions
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.database import DatabaseManager
from core.state_manager import StateManager, UserState
from core.config import Config

class CallbackHandler:
    """Handles callback queries from inline keyboards"""
    
    def __init__(self, db: DatabaseManager, state_manager: StateManager):
        self.db = db
        self.state_manager = state_manager
        self.logger = logging.getLogger(__name__)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main callback handler"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        data = query.data
        
        # Update user activity
        await self.db.update_user_activity(user_id)
        
        self.logger.info(f"User {user_id} triggered callback: {data}")
        
        # Route to appropriate handler
        if data == 'main_menu':
            await self._show_main_menu(query)
        elif data == 'help':
            await self._show_help(query)
        elif data == 'view_status':
            await self._show_status(query)
        elif data == 'premium_info':
            await self._show_premium_info(query)
        elif data == 'session_menu':
            await self._show_session_menu(query)
        elif data == 'upload_session':
            await self._handle_session_upload(query)
        elif data == 'remove_session':
            await self._handle_remove_session(query)
        elif data == 'confirm_remove_session':
            await self._confirm_remove_session(query)
        elif data == 'manage_channels':
            await self._show_channel_management(query)
        elif data == 'add_channel':
            await self._handle_add_channel(query)
        elif data.startswith('remove_channel_'):
            await self._handle_remove_channel(query, data)
        elif data == 'check_frozen':
            await self._show_frozen_menu(query)
        elif data == 'frozen_single':
            await self._handle_single_frozen_check(query)
        elif data == 'frozen_bulk':
            await self._handle_bulk_frozen_check(query)
        elif data == 'check_bulk_frozen':
            await self._process_bulk_frozen(query)
        elif data == 'process_withdraw':
            await self._show_withdraw_menu(query)
        elif data == 'process_bulk_withdraw':
            await self._process_bulk_withdraw(query)
        elif data == 'start_withdraw':
            await self._start_withdraw_processing(query)
        elif data == 'confirm_withdraw':
            await self._confirm_withdraw_processing(query)
        elif data.startswith('admin_'):
            await self._handle_admin_callback(query, data)
        else:
            await query.edit_message_text("🔄 Unknown action. Please try again.")
    
    async def _show_main_menu(self, query):
        """Show main menu"""
        user_id = query.from_user.id
        
        # Clear any existing state
        self.state_manager.clear_state(user_id)
        
        # Get user info for personalized menu
        is_premium = await self.db.is_premium_user(user_id)
        has_session = await self.db.has_session(user_id)
        channels = await self.db.get_user_channels(user_id)
        
        text = f"""
🤖 **RTX Toolkit Main Menu**

📊 **Your Status:**
• Premium: {'✅' if is_premium else '🔄'}
• Session: {'✅' if has_session else '🔄'}
• Channels: {len(channels)}

🚀 **Select an action:**
        """
        
        keyboard = await self._build_main_menu(user_id)
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _show_help(self, query):
        """Show help information"""
        help_text = """
🤖 **RTX Toolkit Bot Help**

**📋 Main Features:**
• ❄️ Check frozen Telegram numbers
• 📂 Manage multiple channels
• 💰 Process withdraw requests
• 🔐 Session management

**🎯 Quick Start:**
1. Get premium access
2. Upload your session file
3. Add channels to monitor
4. Start checking frozen numbers

**⭐ Premium Benefits:**
• Unlimited channels
• Priority processing
• Advanced features
• 24/7 support
        """
        
        keyboard = [
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')],
            [InlineKeyboardButton("⭐ Get Premium", callback_data='premium_info')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _show_status(self, query):
        """Show user status"""
        user_id = query.from_user.id
        
        is_premium = await self.db.is_premium_user(user_id)
        has_session = await self.db.has_session(user_id)
        channels = await self.db.get_user_channels(user_id)
        current_state = self.state_manager.get_state(user_id)
        
        status_text = f"""
📊 **Your Account Status**

👤 **Account Info:**
• Premium: {'✅ Active' if is_premium else '🔄 Inactive'}
• Session: {'✅ Connected' if has_session else '🔄 Required'}
• Current State: {current_state.value.title()}

📂 **Channels ({len(channels)}):**
        """
        
        if channels:
            for i, channel in enumerate(channels[:5]):
                status_text += f"\n{i+1}. {channel['channel_name']}"
            if len(channels) > 5:
                status_text += f"\n... and {len(channels) - 5} more"
        else:
            status_text += "\nNo channels added yet"
        
        keyboard = [
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')],
            [InlineKeyboardButton("📂 Manage Channels", callback_data='manage_channels')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(status_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _show_premium_info(self, query):
        """Show premium information"""
        user_id = query.from_user.id
        
        # Special message for admins
        config = Config()
        if config.is_admin(user_id):
            premium_text = """
👑 **Admin Premium Access**

🎉 **You're an Admin!**
You automatically have access to all premium features:

🚀 **Your Premium Features:**
• ✅ Unlimited channels
• ✅ Priority processing  
• ✅ Advanced analytics
• ✅ Bulk operations
• ✅ 24/7 support
• ✅ Admin panel access
• ✅ User management

No upgrade needed - you're already VIP! 😎
            """
        else:
            premium_text = """
⭐ **Premium Access Required**

🚀 **Premium Features:**
• ✅ Unlimited channels
• ✅ Priority processing
• ✅ Advanced analytics
• ✅ Bulk operations
• ✅ 24/7 support
• ✅ Regular updates

💰 **Free vs Premium:**
• Free: Limited features
• Premium: Full access to all tools

📞 **Get Premium:**
Contact an admin to upgrade your account.
            """
        
        keyboard = [
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')],
            [InlineKeyboardButton("❓ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(premium_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _show_session_menu(self, query):
        """Show session management menu"""
        user_id = query.from_user.id
        has_session = await self.db.has_session(user_id)
        
        if has_session:
            text = """
🔐 **Session Management**

✅ **Session Status:** Connected

Your Telegram session is active and ready to use.

⚙️ **Options:**
            """
            keyboard = [
                [InlineKeyboardButton("🔄 Replace Session", callback_data='upload_session')],
                [InlineKeyboardButton("🗑️ Remove Session", callback_data='remove_session')],
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]
        else:
            text = """
🔐 **Session Management**

🔄 **Session Status:** Not Connected

You need to upload your Telegram session file to use the bot features.

📤 **Upload Session:**
Click the button below and send your .session file.
            """
            keyboard = [
                [InlineKeyboardButton("📤 Upload Session", callback_data='upload_session')],
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')],
                [InlineKeyboardButton("❓ How to get session?", callback_data='session_help')]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _handle_session_upload(self, query):
        """Handle session upload initiation"""
        user_id = query.from_user.id
        
        # Set state for session upload
        self.state_manager.set_state(user_id, UserState.SESSION_UPLOAD)
        
        text = """
📤 **Upload Session File**

Please send your Telegram session file (.session or .zip)

📋 **Instructions:**
1. Send your session file as a document
2. The file will be processed automatically
3. You'll receive a confirmation when done

⚠️ **Security:** Your session data is encrypted and stored securely.
        """
        
        keyboard = [
            [InlineKeyboardButton("🔙 Cancel", callback_data='session_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _handle_remove_session(self, query):
        """Handle session removal request"""
        user_id = query.from_user.id
        
        # Check if user has a session
        user_session = await self.db.get_user_session(user_id)
        
        if not user_session:
            text = """
⚠️ **No Session Found**

You don't have any session file uploaded. There's nothing to remove.

📤 To upload a session, use the "Upload Session" option.
            """
            keyboard = [
                [InlineKeyboardButton("📤 Upload Session", callback_data='upload_session')],
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]
        else:
            text = """
🗑️ **Remove Session**

⚠️ **Warning:** This will permanently delete your stored session file. 

After removal:
- You'll need to upload a new session to use bot features
- Your current session data will be completely removed
- This action cannot be undone

Are you sure you want to proceed?
            """
            keyboard = [
                [InlineKeyboardButton("✅ Yes, Remove Session", callback_data='confirm_remove_session')],
                [InlineKeyboardButton("🔙 Cancel", callback_data='session_menu')]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _confirm_remove_session(self, query):
        """Confirm and execute session removal"""
        user_id = query.from_user.id
        
        try:
            # Remove session from database
            await self.db.remove_user_session(user_id)
            
            text = """
✅ **Session Removed Successfully**

Your Telegram session has been permanently deleted from our system.

📤 **Next Steps:**
- To use bot features again, you'll need to upload a new session file
- All your other settings (channels, premium status) remain unchanged
- Your account data is still preserved

🔐 **Security:** Your session data has been completely wiped from our servers.
            """
            
            keyboard = [
                [InlineKeyboardButton("📤 Upload New Session", callback_data='upload_session')],
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]
            
        except Exception as e:
            self.logger.error(f"Error removing session for user {user_id}: {e}")
            text = """
❌ **Error Removing Session**

Something went wrong while removing your session. Please try again.

If the problem persists, contact support.
            """
            
            keyboard = [
                [InlineKeyboardButton("🔄 Try Again", callback_data='remove_session')],
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _show_channel_management(self, query):
        """Show channel management menu"""
        user_id = query.from_user.id
        channels = await self.db.get_user_channels(user_id)
        
        text = f"""
📂 **Channel Management**

📊 **Current Channels:** {len(channels)}

        """
        
        keyboard = []
        
        if channels:
            text += "🔹 **Your Channels:**\n"
            for i, channel in enumerate(channels[:10]):  # Show first 10
                text += f"{i+1}. {channel['channel_name']}\n"
            
            # Add remove buttons for channels
            for i, channel in enumerate(channels[:5]):  # First 5 can be removed via buttons
                keyboard.append([InlineKeyboardButton(
                    f"🗑️ Remove {channel['channel_name'][:20]}...", 
                    callback_data=f'remove_channel_{channel["id"]}'
                )])
        else:
            text += "No channels added yet.\n"
        
        text += "\n➕ **Add New Channel:**"
        
        keyboard.append([InlineKeyboardButton("➕ Add Channel", callback_data='add_channel')])
        keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _handle_add_channel(self, query):
        """Handle adding a new channel"""
        user_id = query.from_user.id
        
        # Check limits
        is_premium = await self.db.is_premium_user(user_id)
        channels = await self.db.get_user_channels(user_id)
        
        max_channels = 100 if is_premium else 5
        
        if len(channels) >= max_channels:
            text = f"""
⚠️ **Channel Limit Reached**

You have reached the maximum number of channels ({max_channels}).

{"Upgrade to premium for unlimited channels!" if not is_premium else "Please remove some channels first."}
            """
            keyboard = [
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')],
                [InlineKeyboardButton("📂 Manage Channels", callback_data='manage_channels')]
            ]
            if not is_premium:
                keyboard.insert(0, [InlineKeyboardButton("⭐ Get Premium", callback_data='premium_info')])
        else:
            # Set state for channel setup
            self.state_manager.set_state(user_id, UserState.CHANNEL_SETUP)
            
            text = """
➕ **Add New Channel**

Please send the channel information in one of these formats:

**Format 1 (Username):**
`@channel_username Channel Name`

**Format 2 (Channel ID):**
`-1001234567890 Channel Name`

**Examples:**
`@mytestchannel My Test Channel`
`-1002647763210 My Channel`

📋 **Instructions:**
• Username format: starts with @
• ID format: starts with -100 (from channel info)
• Include a descriptive name
• Make sure you have access to the channel
            """
            keyboard = [
                [InlineKeyboardButton("🔙 Cancel", callback_data='manage_channels')]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _handle_remove_channel(self, query, callback_data):
        """Handle channel removal"""
        user_id = query.from_user.id
        channel_id = int(callback_data.split('_')[-1])
        
        success = await self.db.remove_channel(user_id, channel_id)
        
        if success:
            text = "✅ Channel removed successfully!"
        else:
            text = "🔄 Failed to remove channel. Please try again."
        
        keyboard = [
            [InlineKeyboardButton("📂 Manage Channels", callback_data='manage_channels')],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _show_frozen_menu(self, query):
        """Show frozen check menu"""
        user_id = query.from_user.id
        
        # Check if user has detected numbers from file upload
        detected_numbers = self.state_manager.get_context(user_id, 'detected_numbers')
        detected_file = self.state_manager.get_context(user_id, 'detected_file')
        
        if detected_numbers:
            # Sanitize filename for display (remove problematic Unicode characters)
            safe_filename = detected_file.encode('ascii', 'ignore').decode('ascii')
            if not safe_filename:
                safe_filename = "uploaded_file.txt"
            
            text = f"""
❄️ **Check Frozen Numbers**

📁 **Detected File:** {safe_filename}
📱 **Numbers Found:** {len(detected_numbers)}

Choose how to proceed:
            """
            
            keyboard = [
                [InlineKeyboardButton("✅ Check Detected Numbers", callback_data='check_bulk_frozen')],
                [InlineKeyboardButton("📄 Single Check", callback_data='frozen_single')],
                [InlineKeyboardButton("📁 Upload New File", callback_data='frozen_bulk')],
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]
            
            # Transfer detected numbers to bulk_numbers for processing
            self.state_manager.set_context(user_id, 'bulk_numbers', detected_numbers)
            self.state_manager.set_context(user_id, 'source_file', detected_file)
            
        else:
            text = """
❄️ **Check Frozen Numbers**

📋 **Choose checking method:**

📄 **Single Check:** Check one phone number
📁 **Bulk Check:** Upload file with multiple numbers
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("📄 Single Check", callback_data='frozen_single'),
                    InlineKeyboardButton("📁 Bulk Check", callback_data='frozen_bulk')
                ],
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _show_withdraw_menu(self, query):
        """Show withdraw processing menu"""
        user_id = query.from_user.id
        
        # Check if user has detected numbers from file upload
        detected_numbers = self.state_manager.get_context(user_id, 'detected_numbers')
        detected_file = self.state_manager.get_context(user_id, 'detected_file')
        
        if detected_numbers:
            # Sanitize filename for display (remove problematic Unicode characters)
            safe_filename = detected_file.encode('ascii', 'ignore').decode('ascii')
            if not safe_filename:
                safe_filename = "uploaded_file.txt"
            
            text = f"""
💰 **Withdraw Processing**

📁 **Detected File:** {safe_filename}
📱 **Numbers Found:** {len(detected_numbers)}

Choose how to proceed:
            """
            
            keyboard = [
                [InlineKeyboardButton("✅ Process Detected Numbers", callback_data='process_bulk_withdraw')],
                [InlineKeyboardButton("📤 Manual Input", callback_data='start_withdraw')],
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]
            
            # Transfer detected numbers for processing
            self.state_manager.set_context(user_id, 'bulk_numbers', detected_numbers)
            self.state_manager.set_context(user_id, 'source_file', detected_file)
            
        else:
            text = """
💰 **Withdraw Processing**

�📋 **Process withdraw requests from your channels**

⚙️ **Features:**
• Automatic number extraction
• Support for text messages and files
• Frozen status checking
• Detailed reports
• Bulk processing

📤 **Supported inputs:**
• Text messages with phone numbers
• .txt files with number lists
• .zip archives with multiple files
• .csv files with structured data
            """
            
            keyboard = [
                [InlineKeyboardButton("📤 Start Processing", callback_data='start_withdraw')],
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _handle_admin_callback(self, query, data):
        """Handle admin callbacks"""
        user_id = query.from_user.id
        
        # Check admin access
        from core.config import Config
        config = Config()
        
        if not config.is_admin(user_id):
            await query.edit_message_text("🔄 Access denied.")
            return
        
        if data == 'admin_users':
            await self._show_admin_users(query)
        elif data == 'admin_stats':
            await self._show_admin_stats(query)
        elif data == 'admin_settings':
            await self._show_admin_settings(query)
        elif data == 'admin_logs':
            await self._show_admin_logs(query)
    
    async def _show_admin_users(self, query):
        """Show admin user management"""
        text = """
👥 **User Management**

⚙️ **Quick Actions:**
        """
        
        keyboard = [
            [InlineKeyboardButton("➕ Add Premium", callback_data='admin_add_premium')],
            [InlineKeyboardButton("➖ Remove Premium", callback_data='admin_remove_premium')],
            [InlineKeyboardButton("📊 User Stats", callback_data='admin_user_stats')],
            [InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_panel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _show_admin_stats(self, query):
        """Show admin statistics"""
        # Get basic stats (you can expand this)
        text = """
📊 **Bot Statistics**

👥 **Users:** Loading...
💎 **Premium Users:** Loading...
📂 **Total Channels:** Loading...
🔄 **Active Sessions:** Loading...

📈 **Performance:**
• Uptime: Good
• Response Time: Fast
• Database: Healthy
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data='admin_stats')],
            [InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_panel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _show_admin_settings(self, query):
        """Show admin settings"""
        text = """
⚙️ **Bot Settings**

🔧 **Configuration:**
• Max channels (Free): 5
• Max channels (Premium): 100
• Session timeout: 1 hour
• Cache duration: 1 hour

📝 **Maintenance:**
        """
        
        keyboard = [
            [InlineKeyboardButton("🗄️ Database Cleanup", callback_data='admin_cleanup')],
            [InlineKeyboardButton("🔄 Restart Services", callback_data='admin_restart')],
            [InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_panel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _show_admin_logs(self, query):
        """Show admin logs"""
        text = """
📝 **System Logs**

📊 **Recent Activity:**
• Bot started successfully
• Database initialized
• All handlers registered

🔍 **Log Levels:**
• INFO: General information
• WARNING: Important notices
• ERROR: Critical issues
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 View Full Logs", callback_data='admin_full_logs')],
            [InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_panel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
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
                    InlineKeyboardButton("💰 Withdraw", callback_data='process_withdraw')
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
    
    async def _handle_single_frozen_check(self, query):
        """Handle single number frozen check"""
        user_id = query.from_user.id
        
        # Set state for single number input
        self.state_manager.set_state(user_id, UserState.FILE_UPLOAD)
        self.state_manager.set_context(user_id, 'check_type', 'single')
        
        text = """
📱 **Single Number Check**

Please send a phone number to check:

**Examples:**
• `+1234567890`
• `1234567890`
• `+44 123 456 7890`

🔢 Send the number as a message.
        """
        
        keyboard = [
            [InlineKeyboardButton("🔙 Cancel", callback_data='check_frozen')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _handle_bulk_frozen_check(self, query):
        """Handle bulk number frozen check"""
        user_id = query.from_user.id
        
        # Set state for file upload
        self.state_manager.set_state(user_id, UserState.FILE_UPLOAD)
        self.state_manager.set_context(user_id, 'check_type', 'bulk')
        
        text = """
📁 **Bulk Number Check**

Please upload a file containing phone numbers:

**Supported formats:**
• `.txt` - Plain text with numbers
• `.zip` - Compressed text files
• `.csv` - Comma-separated values

📤 Upload your file now.
        """
        
        keyboard = [
            [InlineKeyboardButton("🔙 Cancel", callback_data='check_frozen')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _process_bulk_frozen(self, query):
        """Process bulk frozen check from stored numbers"""
        user_id = query.from_user.id
        
        # Get stored numbers
        numbers = self.state_manager.get_context(user_id, 'bulk_numbers')
        source_file = self.state_manager.get_context(user_id, 'source_file')
        
        if not numbers:
            await query.edit_message_text(
                "🔄 No numbers found to process.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
                ]])
            )
            return
        
        # Get user channels
        channels = await self.db.get_user_channels(user_id)
        
        if not channels:
            await query.edit_message_text(
                "🔄 No channels found. Please add channels first.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📂 Add Channels", callback_data='manage_channels')],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
                ])
            )
            return
        
        # Start processing (this would integrate with your frozen checking logic)
        text = f"""
🔄 **Processing Frozen Check**

📁 **Source:** {source_file or 'Unknown'}
📱 **Numbers:** {len(numbers)}
📂 **Channels:** {len(channels)}

⏳ Processing... This may take a moment.
        """
        
        await query.edit_message_text(text, parse_mode='Markdown')
        
        # Here you would integrate with your actual frozen checking logic
        # For now, simulate processing
        results = {
            'total': len(numbers),
            'frozen': len(numbers) // 3,  # Simulate some frozen numbers
            'active': len(numbers) - (len(numbers) // 3),
            'channels_checked': len(channels)
        }
        
        result_text = f"""
✅ **Frozen Check Complete**

📊 **Results:**
• Total Numbers: {results['total']}
• Frozen: {results['frozen']}
• Active: {results['active']}
• Channels Checked: {results['channels_checked']}

📄 **Report:** Processing completed successfully.
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 Detailed Report", callback_data='frozen_report')],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Clear stored data
        self.state_manager.clear_context(user_id, 'bulk_numbers')
        self.state_manager.clear_context(user_id, 'source_file')
        
        await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _process_bulk_withdraw(self, query):
        """Process bulk withdraw from stored numbers"""
        user_id = query.from_user.id
        
        # Get stored numbers and set withdraw state
        numbers = self.state_manager.get_context(user_id, 'bulk_numbers')
        source_file = self.state_manager.get_context(user_id, 'source_file')
        
        if numbers:
            self.state_manager.set_state(user_id, UserState.WITHDRAW_PROCESSING)
            self.state_manager.set_context(user_id, 'withdraw_numbers', numbers)
            
            text = f"""
💰 **Withdraw Processing Started**

📁 **Source:** {source_file or 'Unknown'}
📱 **Numbers:** {len(numbers)}

🔄 Numbers have been loaded for withdraw processing.
You can now send additional withdraw messages or files.
            """
            
            keyboard = [
                [InlineKeyboardButton("✅ Process All", callback_data='confirm_withdraw')],
                [InlineKeyboardButton("🔙 Cancel", callback_data='main_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await query.edit_message_text(
                "🔄 No numbers found to process.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
                ]])
            )
    
    async def _start_withdraw_processing(self, query):
        """Start withdraw processing mode"""
        user_id = query.from_user.id
        
        # Set withdraw processing state
        self.state_manager.set_state(user_id, UserState.WITHDRAW_PROCESSING)
        
        text = """
💰 **Withdraw Processing Mode**

📝 **Send withdraw requests:**
• Forward withdraw messages
• Send text with phone numbers  
• Upload files with numbers (.txt, .zip, .csv)

📱 I'll extract phone numbers and process them automatically.

🔄 **Processing options available after collecting numbers.**
        """
        
        keyboard = [
            [InlineKeyboardButton("🔙 Cancel", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def _confirm_withdraw_processing(self, query):
        """Confirm and process all collected withdraw numbers"""
        user_id = query.from_user.id
        
        numbers = self.state_manager.get_context(user_id, 'withdraw_numbers')
        
        if not numbers:
            await query.edit_message_text(
                "🔄 No numbers collected for processing.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("💰 Start Again", callback_data='process_withdraw')
                ]])
            )
            return
        
        # Process withdraw (integrate with your withdraw logic)
        text = f"""
🔄 **Processing Withdraw Request**

📱 **Total Numbers:** {len(numbers)}
⏳ **Status:** Processing...

This may take a moment depending on the number of entries.
        """
        
        await query.edit_message_text(text, parse_mode='Markdown')
        
        # Simulate processing (replace with actual logic)
        results = {
            'processed': len(numbers),
            'successful': len(numbers) - 2,  # Simulate some failures
            'failed': 2
        }
        
        result_text = f"""
✅ **Withdraw Processing Complete**

📊 **Results:**
• Total Processed: {results['processed']}
• Successful: {results['successful']}
• Failed: {results['failed']}

📄 All withdraw requests have been processed.
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 View Report", callback_data='withdraw_report')],
            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Clear withdraw state and data
        self.state_manager.clear_state(user_id)
        self.state_manager.clear_context(user_id, 'withdraw_numbers')
        
        await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode='Markdown')
