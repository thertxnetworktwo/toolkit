"""
Message handler for state-based text and document processing
"""

import logging
import re
import aiofiles
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.database import DatabaseManager
from core.state_manager import StateManager, UserState

class MessageHandler:
    """Handles text messages and documents based on user state"""
    
    def __init__(self, db: DatabaseManager, state_manager: StateManager):
        self.db = db
        self.state_manager = state_manager
        self.logger = logging.getLogger(__name__)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe display in Telegram messages"""
        if not filename:
            return "unknown_file"
        
        # Replace problematic Unicode characters that break Telegram entity parsing
        # These are mathematical bold/italic Unicode characters that cause issues
        replacements = {
            # Mathematical Bold characters
            '𝐀': 'A', '𝐁': 'B', '𝐂': 'C', '𝐃': 'D', '𝐄': 'E', '𝐅': 'F', '𝐆': 'G', '𝐇': 'H',
            '𝐈': 'I', '𝐉': 'J', '𝐊': 'K', '𝐋': 'L', '𝐌': 'M', '𝐍': 'N', '𝐎': 'O', '𝐏': 'P',
            '𝐐': 'Q', '𝐑': 'R', '𝐒': 'S', '𝐓': 'T', '𝐔': 'U', '𝐕': 'V', '𝐖': 'W', '𝐗': 'X',
            '𝐘': 'Y', '𝐙': 'Z', '𝐚': 'a', '𝐛': 'b', '𝐜': 'c', '𝐝': 'd', '𝐞': 'e', '𝐟': 'f',
            '𝐠': 'g', '𝐡': 'h', '𝐢': 'i', '𝐣': 'j', '𝐤': 'k', '𝐥': 'l', '𝐦': 'm', '𝐧': 'n',
            '𝐨': 'o', '𝐩': 'p', '𝐪': 'q', '𝐫': 'r', '𝐬': 's', '𝐭': 't', '𝐮': 'u', '𝐯': 'v',
            '𝐰': 'w', '𝐱': 'x', '𝐲': 'y', '𝐳': 'z',
            # Mathematical Bold Italic
            '𝒆': 'e', '𝒐': 'o', '𝒏': 'n', '𝒊': 'i', '𝒗': 'v', '𝒓': 'r', '𝒕': 't',
            # Other problematic characters
            '🤖': 'BOT', '𝐂𝐨𝐧𝐯𝐞𝐫𝐭': 'Convert'
        }
        
        safe_name = filename
        for unicode_char, replacement in replacements.items():
            safe_name = safe_name.replace(unicode_char, replacement)
        
        # If still contains problematic characters, fall back to ASCII-only
        try:
            # Test if the string can be safely encoded/decoded
            safe_name.encode('utf-8').decode('utf-8')
        except UnicodeError:
            safe_name = filename.encode('ascii', 'ignore').decode('ascii')
        
        if not safe_name or safe_name.strip() == "":
            safe_name = "uploaded_file"
        
        return safe_name
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages based on user state"""
        # Check if update has effective_user (can be None for channel posts)
        if not update.effective_user:
            self.logger.warning("Received update without effective_user, ignoring")
            return
            
        user_id = update.effective_user.id
        
        # Check if message exists
        if not update.message or not update.message.text:
            self.logger.warning(f"User {user_id} sent update without text message")
            return
            
        text = update.message.text
        current_state = self.state_manager.get_state(user_id)
        
        self.logger.info(f"User {user_id} sent text in state {current_state.value}: {text[:50]}...")
        
        # Check if user is registered
        if not await self.db.is_user_registered(user_id):
            await update.message.reply_text(
                "Please start the bot first using /start",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🚀 Start Bot", callback_data='main_menu')
                ]])
            )
            return
        
        # Route based on current state
        if current_state == UserState.CHANNEL_SETUP:
            await self._handle_channel_setup(update, text)
        elif current_state == UserState.WITHDRAW_PROCESSING:
            await self._handle_withdraw_message(update, text)
        elif current_state == UserState.ADMIN_COMMAND:
            await self._handle_admin_input(update, text)
        else:
            # Default state - provide guidance
            await self._handle_default_message(update, text)
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document uploads based on user state"""
        # Check if update has effective_user (can be None for channel posts)
        if not update.effective_user:
            self.logger.warning("Received document update without effective_user, ignoring")
            return
            
        user_id = update.effective_user.id
        
        # Check if message and document exist
        if not update.message or not update.message.document:
            self.logger.warning(f"User {user_id} sent update without document")
            return
            
        document = update.message.document
        current_state = self.state_manager.get_state(user_id)
        
        filename = document.file_name.lower() if document.file_name else ""
        safe_filename = self._sanitize_filename(filename)
        self.logger.info(f"User {user_id} uploaded document in state {current_state.value}: {safe_filename}")
        
        # Check if user is registered
        if not await self.db.is_user_registered(user_id):
            await update.message.reply_text("Please start the bot first using /start")
            return
        
        # Route based on current state
        if current_state == UserState.SESSION_UPLOAD:
            await self._handle_session_file(update, document)
        elif current_state == UserState.FILE_UPLOAD:
            await self._handle_number_file(update, document)
        elif current_state == UserState.WITHDRAW_PROCESSING:
            # Allow file uploads during withdraw processing
            if filename.endswith(('.txt', '.zip')):
                await self._handle_withdraw_file(update, document)
            else:
                await self._handle_unexpected_file(update, document)
        else:
            # Smart file type detection for idle users
            await self._handle_smart_file_detection(update, document)
    
    async def _handle_channel_setup(self, update: Update, text: str):
        """Handle channel setup input"""
        user_id = update.effective_user.id
        
        # Parse channel input: supports both @username Channel Name and -1001234567890 Channel Name
        text = text.strip()
        
        # Check for username format: @username Channel Name
        username_match = re.match(r'^@([a-zA-Z0-9_]+)\s+(.+)$', text)
        # Check for channel ID format: -1001234567890 Channel Name
        id_match = re.match(r'^(-100\d{10,})\s+(.+)$', text)
        
        if username_match:
            channel_username = username_match.group(1)
            channel_name = username_match.group(2)
            channel_id = f"@{channel_username}"
        elif id_match:
            channel_id = id_match.group(1)
            channel_name = id_match.group(2)
        else:
            await update.message.reply_text(
                "⚠️ **Invalid Format**\\n\\n"
                "Please use one of these formats:\\n"
                "`@channel_username Channel Name`\\n"
                "`-1001234567890 Channel Name`\\n\\n"
                "**Examples:**\\n"
                "`@mytestchannel My Test Channel`\\n"
                "`-1002647763210 My Channel`",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Cancel", callback_data='manage_channels')
                ]])
            )
            return
        
        # Validate channel name length
        if len(channel_name) > 100:
            await update.message.reply_text(
                "🔄 Channel name is too long. Please use a shorter name.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Cancel", callback_data='manage_channels')
                ]])
            )
            return
        
        # Check if channel already exists
        channels = await self.db.get_user_channels(user_id)
        if any(ch['channel_id'].lower() == channel_id.lower() for ch in channels):
            await update.message.reply_text(
                "🔄 This channel is already added to your list.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📂 Manage Channels", callback_data='manage_channels')
                ]])
            )
            return
        
        # Add channel to database
        success = await self.db.add_channel(user_id, channel_id, channel_name)
        
        if success:
            # Clear state
            self.state_manager.clear_state(user_id)
            
            await update.message.reply_text(
                f"✅ **Channel Added Successfully!**\\n\\n"
                f"📂 **Channel:** {channel_name}\\n"
                f"🔗 **ID:** {channel_id}\\n\\n"
                f"You can now use this channel for checking frozen numbers.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📂 Manage Channels", callback_data='manage_channels')],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
                ])
            )
        else:
            await update.message.reply_text(
                "🔄 Failed to add channel. Please try again.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📂 Manage Channels", callback_data='manage_channels')
                ]])
            )
    
    async def _handle_withdraw_message(self, update: Update, text: str):
        """Handle withdraw processing messages"""
        user_id = update.effective_user.id
        
        # Extract phone numbers from text
        phone_numbers = self._extract_phone_numbers(text)
        
        if not phone_numbers:
            await update.message.reply_text(
                "🔄 No phone numbers found in the message.\\n\\n"
                "Please send a message containing phone numbers to process.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Cancel", callback_data='main_menu')
                ]])
            )
            return
        
        # Process the numbers (this would be expanded with actual frozen checking)
        result_text = f"📱 **Found {len(phone_numbers)} phone numbers:**\\n\\n"
        for i, number in enumerate(phone_numbers[:10], 1):  # Show first 10
            result_text += f"{i}. `{number}`\\n"
        
        if len(phone_numbers) > 10:
            result_text += f"\\n... and {len(phone_numbers) - 10} more numbers"
        
        result_text += "\\n\\n🔄 Processing withdraw request..."
        
        await update.message.reply_text(
            result_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirm Processing", callback_data='confirm_withdraw')],
                [InlineKeyboardButton("🔙 Cancel", callback_data='main_menu')]
            ])
        )
        
        # Store numbers in context for processing
        self.state_manager.set_context(user_id, 'withdraw_numbers', phone_numbers)
    
    async def _handle_admin_input(self, update: Update, text: str):
        """Handle admin command input"""
        user_id = update.effective_user.id
        
        # Check admin access
        from core.config import Config
        config = Config()
        
        if not config.is_admin(user_id):
            self.state_manager.clear_state(user_id)
            await update.message.reply_text("🔄 Access denied.")
            return
        
        # Process admin input based on context
        admin_action = self.state_manager.get_context(user_id, 'admin_action')
        
        if admin_action == 'add_premium':
            await self._process_add_premium(update, text)
        elif admin_action == 'remove_premium':
            await self._process_remove_premium(update, text)
        else:
            await update.message.reply_text("🔄 Unknown admin action.")
            self.state_manager.clear_state(user_id)
    
    async def _handle_default_message(self, update: Update, text: str):
        """Handle messages when user is in default state"""
        # Check if it looks like a phone number list (for quick processing)
        phone_numbers = self._extract_phone_numbers(text)
        
        if phone_numbers:
            # User sent phone numbers - offer to process them
            await update.message.reply_text(
                f"📱 I found {len(phone_numbers)} phone numbers in your message.\\n\\n"
                f"Would you like to check them for frozen status?",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("❄️ Check Frozen", callback_data='check_frozen')],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
                ])
            )
        else:
            # Default response
            await update.message.reply_text(
                "🤖 I'm not sure what you want to do.\\n\\n"
                "Please use the menu buttons for easy navigation.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
                ]])
            )
    
    async def _handle_session_file(self, update: Update, document):
        """Handle session file upload (.session, .zip, .tdata)"""
        user_id = update.effective_user.id
        
        # Check file type
        filename = document.file_name.lower() if document.file_name else ""
        
        # Supported session file types
        supported_types = ['.session', '.zip', '.tdata', '.json']
        
        if not any(filename.endswith(ext) for ext in supported_types):
            await update.message.reply_text(
                "⚠️ **Invalid File Type**\\n\\n"
                "**Supported session files:**\\n"
                "• `.session` - Telethon session files\\n"
                "• `.zip` - Compressed session archives\\n"
                "• `.tdata` - Telegram Desktop data\\n"
                "• `.json` - Session data exports",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔐 Session Menu", callback_data='session_menu')
                ]])
            )
            return
        
        # Download and process file
        try:
            file = await document.get_file()
            
            # Create temp directory
            temp_dir = Path(__file__).parent.parent / 'data' / 'temp'
            temp_dir.mkdir(exist_ok=True)
            
            # Download file
            temp_file = temp_dir / f"session_{user_id}_{document.file_name}"
            await file.download_to_drive(temp_file)
            
            # Process based on file type
            if filename.endswith('.zip'):
                session_data = await self._process_zip_session(temp_file, user_id)
            else:
                # Read file content directly
                async with aiofiles.open(temp_file, 'rb') as f:
                    session_data = await f.read()
            
            if session_data:
                # Store in database
                success = await self.db.store_session(user_id, session_data, filename)
                
                # Clean up temp file
                temp_file.unlink(missing_ok=True)
                
                if success:
                    # Clear state
                    self.state_manager.clear_state(user_id)
                    
                    await update.message.reply_text(
                        "✅ **Session Uploaded Successfully!**\\n\\n"
                        f"🔐 File: {self._sanitize_filename(document.file_name)}\\n"
                        "📱 Your Telegram session is now connected.\\n"
                        "You can start using all bot features.",
                        parse_mode='Markdown',
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')],
                            [InlineKeyboardButton("📂 Add Channels", callback_data='manage_channels')]
                        ])
                    )
                else:
                    await update.message.reply_text(
                        "🔄 Failed to store session. Please try again.",
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton("🔐 Session Menu", callback_data='session_menu')
                        ]])
                    )
            else:
                temp_file.unlink(missing_ok=True)
                await update.message.reply_text(
                    "🔄 Could not extract session data from file.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🔐 Session Menu", callback_data='session_menu')
                    ]])
                )
        
        except Exception as e:
            self.logger.error(f"Session upload error for user {user_id}: {e}")
            await update.message.reply_text(
                "🔄 Error processing session file. Please try again.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔐 Session Menu", callback_data='session_menu')
                ]])
            )
    
    async def _handle_number_file(self, update: Update, document):
        """Handle phone number file upload (.txt only for frozen check)"""
        user_id = update.effective_user.id
        
        # Check file type - Only TXT files allowed for frozen checking
        filename = document.file_name.lower() if document.file_name else ""
        
        if not filename.endswith('.txt'):
            await update.message.reply_text(
                "⚠️ **Invalid File Type for Frozen Check**\\n\\n"
                "**For frozen status checking, only TXT files are supported:**\\n"
                "• `.txt` - Plain text with phone numbers\\n\\n"
                "Please upload a `.txt` file containing phone numbers.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
                ]])
            )
            return
        
        try:
            file = await document.get_file()
            
            # Handle TXT files only
            file_content = await file.download_as_bytearray()
            text_content = file_content.decode('utf-8', errors='ignore')
            phone_numbers = self._extract_phone_numbers(text_content)
            
            if not phone_numbers:
                await update.message.reply_text(
                    "🔄 No phone numbers found in the file.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')
                    ]])
                )
                return
            
            # Store numbers for processing
            self.state_manager.set_context(user_id, 'bulk_numbers', phone_numbers)
            self.state_manager.set_context(user_id, 'source_file', document.file_name)
            
            await update.message.reply_text(
                f"✅ **File Processed Successfully!**\\n\\n"
                f"📄 **File:** {self._sanitize_filename(document.file_name)}\\n"
                f"📱 **Found:** {len(phone_numbers)} phone numbers\\n\\n"
                f"🔄 Ready to check frozen status.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("❄️ Check All Frozen", callback_data='check_bulk_frozen')],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
                ])
            )
        
        except Exception as e:
            self.logger.error(f"File processing error for user {user_id}: {e}")
            await update.message.reply_text("🔄 Error processing file. Please try again.")
    
    async def _handle_unexpected_file(self, update: Update, document):
        """Handle unexpected file uploads"""
        await update.message.reply_text(
            "🤖 **File Received**\\n\\n"
            "I'm not sure what to do with this file.\\n"
            "Please use the menu to specify your action first.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔐 Session Upload", callback_data='session_menu')],
                [InlineKeyboardButton("❄️ Check Frozen", callback_data='check_frozen')],
                [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
            ])
        )
    
    async def _process_add_premium(self, update: Update, text: str):
        """Process add premium admin command"""
        user_id = update.effective_user.id
        
        # Extract target user ID
        try:
            target_user_id = int(text.strip())
        except ValueError:
            await update.message.reply_text(
                "🔄 Invalid user ID. Please send a valid user ID number.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_users')
                ]])
            )
            return
        
        # Set premium status
        success = await self.db.set_premium_status(target_user_id, True)
        
        if success:
            await update.message.reply_text(
                f"✅ User {target_user_id} has been granted premium access.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_users')
                ]])
            )
        else:
            await update.message.reply_text(
                f"🔄 Failed to grant premium access to user {target_user_id}.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_users')
                ]])
            )
        
        # Clear admin state
        self.state_manager.clear_state(user_id)
    
    async def _process_remove_premium(self, update: Update, text: str):
        """Process remove premium admin command"""
        user_id = update.effective_user.id
        
        # Extract target user ID
        try:
            target_user_id = int(text.strip())
        except ValueError:
            await update.message.reply_text(
                "🔄 Invalid user ID. Please send a valid user ID number.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_users')
                ]])
            )
            return
        
        # Remove premium status
        success = await self.db.set_premium_status(target_user_id, False)
        
        if success:
            await update.message.reply_text(
                f"✅ Premium access removed from user {target_user_id}.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_users')
                ]])
            )
        else:
            await update.message.reply_text(
                f"🔄 Failed to remove premium access from user {target_user_id}.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Admin Panel", callback_data='admin_users')
                ]])
            )
        
        # Clear admin state
        self.state_manager.clear_state(user_id)
    
    def _extract_phone_numbers(self, text: str) -> list:
        """Extract phone numbers from text"""
        # Pattern for various phone number formats
        patterns = [
            r'\+\d{10,15}',  # +1234567890
            r'\d{10,15}',    # 1234567890
            r'\d{1,4}[-\s]\d{3,4}[-\s]\d{3,4}[-\s]\d{3,4}',  # 1-234-567-8900
        ]
        
        phone_numbers = []
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Clean the number
                cleaned = re.sub(r'[-\s]', '', match)
                if 10 <= len(cleaned) <= 15:  # Reasonable phone number length
                    phone_numbers.append(cleaned)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_numbers = []
        for number in phone_numbers:
            if number not in seen:
                seen.add(number)
                unique_numbers.append(number)
        
        return unique_numbers
    
    async def _process_zip_session(self, zip_path: Path, user_id: int) -> bytes:
        """Process ZIP file to extract session data"""
        import zipfile
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Look for session files in the ZIP
                session_files = [f for f in zip_ref.namelist() 
                               if f.lower().endswith(('.session', '.tdata', '.json'))]
                
                if not session_files:
                    self.logger.warning(f"No session files found in ZIP for user {user_id}")
                    return None
                
                # Use the first session file found
                session_file = session_files[0]
                session_data = zip_ref.read(session_file)
                
                self.logger.info(f"Extracted session file {session_file} from ZIP for user {user_id}")
                return session_data
                
        except Exception as e:
            self.logger.error(f"Error processing ZIP session for user {user_id}: {e}")
            return None
    
    async def _extract_numbers_from_zip(self, file, user_id: int) -> list:
        """Extract phone numbers from ZIP file containing text files"""
        import zipfile
        from io import BytesIO
        
        try:
            # Download ZIP content
            zip_content = await file.download_as_bytearray()
            
            phone_numbers = []
            
            with zipfile.ZipFile(BytesIO(zip_content), 'r') as zip_ref:
                # Process all text files in the ZIP
                for file_info in zip_ref.infolist():
                    if not file_info.is_dir() and file_info.filename.lower().endswith(('.txt', '.csv')):
                        try:
                            file_content = zip_ref.read(file_info.filename)
                            text_content = file_content.decode('utf-8', errors='ignore')
                            numbers = self._extract_phone_numbers(text_content)
                            phone_numbers.extend(numbers)
                            self.logger.info(f"Extracted {len(numbers)} numbers from {file_info.filename}")
                        except Exception as e:
                            self.logger.warning(f"Error processing file {file_info.filename}: {e}")
            
            # Remove duplicates
            unique_numbers = list(dict.fromkeys(phone_numbers))
            return unique_numbers
            
        except Exception as e:
            self.logger.error(f"Error extracting numbers from ZIP for user {user_id}: {e}")
            return []
    
    async def _handle_withdraw_file(self, update: Update, document):
        """Handle file upload during withdraw processing"""
        user_id = update.effective_user.id
        filename = document.file_name.lower() if document.file_name else ""
        
        try:
            file = await document.get_file()
            phone_numbers = []
            
            if filename.endswith('.zip'):
                phone_numbers = await self._extract_numbers_from_zip(file, user_id)
            else:
                # Handle single text file
                file_content = await file.download_as_bytearray()
                text_content = file_content.decode('utf-8', errors='ignore')
                phone_numbers = self._extract_phone_numbers(text_content)
            
            if phone_numbers:
                # Store for withdraw processing
                existing_numbers = self.state_manager.get_context(user_id, 'withdraw_numbers') or []
                all_numbers = existing_numbers + phone_numbers
                unique_numbers = list(dict.fromkeys(all_numbers))  # Remove duplicates
                
                self.state_manager.set_context(user_id, 'withdraw_numbers', unique_numbers)
                
                await update.message.reply_text(
                    f"✅ **File Added to Withdraw Processing**\\n\\n"
                    f"📁 **File:** {self._sanitize_filename(document.file_name)}\\n"
                    f"📱 **New Numbers:** {len(phone_numbers)}\\n"
                    f"📊 **Total Numbers:** {len(unique_numbers)}\\n\\n"
                    f"🔄 Ready to process withdraw request.",
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("✅ Process All", callback_data='confirm_withdraw')],
                        [InlineKeyboardButton("🔙 Cancel", callback_data='main_menu')]
                    ])
                )
            else:
                await update.message.reply_text(
                    "🔄 No phone numbers found in the file.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🔄 Try Again", callback_data='process_withdraw')
                    ]])
                )
        
        except Exception as e:
            self.logger.error(f"Withdraw file processing error for user {user_id}: {e}")
            await update.message.reply_text("🔄 Error processing file.")
    
    async def _handle_smart_file_detection(self, update: Update, document):
        """Smart file type detection for users not in specific states"""
        user_id = update.effective_user.id
        filename = document.file_name.lower() if document.file_name else ""
        
        # Detect file type and suggest appropriate action
        if filename.endswith(('.session', '.tdata', '.json')):
            # Session file detected
            await update.message.reply_text(
                "📤 **Session File Detected**\\n\\n"
                f"📁 File: {self._sanitize_filename(document.file_name)}\\n\\n"
                "Would you like to upload this as your session file?",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔐 Upload Session", callback_data='upload_session')],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
                ])
            )
        elif filename.endswith(('.txt', '.csv', '.zip')):
            # Number file detected
            file = await document.get_file()
            
            # Quick scan for phone numbers
            if filename.endswith('.zip'):
                phone_numbers = await self._extract_numbers_from_zip(file, user_id)
            else:
                file_content = await file.download_as_bytearray()
                text_content = file_content.decode('utf-8', errors='ignore')
                phone_numbers = self._extract_phone_numbers(text_content)
            
            if phone_numbers:
                await update.message.reply_text(
                    f"📱 **Phone Numbers Detected**\\n\\n"
                    f"📁 File: {self._sanitize_filename(document.file_name)}\\n"
                    f"📊 Found: {len(phone_numbers)} numbers\\n\\n"
                    f"What would you like to do?",
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("❄️ Check Frozen", callback_data='check_frozen')],
                        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
                    ])
                )
                # Store numbers for potential use
                self.state_manager.set_context(user_id, 'detected_numbers', phone_numbers)
                self.state_manager.set_context(user_id, 'detected_file', document.file_name)
            else:
                await self._handle_unexpected_file(update, document)
        else:
            await self._handle_unexpected_file(update, document)
