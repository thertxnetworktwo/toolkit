# RTX Toolkit Bot

A professional Telegram bot for phone number management and frozen status checking with advanced state management architecture.

## 🚀 Features

### Core Functionality
- **📱 Phone Number Processing**: Extract and process phone numbers from various file formats
- **❄️ Frozen Status Checking**: Check if phone numbers are frozen on Telegram
- **🔐 Session Management**: Upload and manage Telegram session files
- **📂 Channel Management**: Add and manage multiple Telegram channels
- **💰 Withdraw Processing**: Process withdraw requests for phone numbers

### Advanced Features
- **🎯 State Management**: Professional state-based handler system prevents conflicts
- **📁 File Support**: TXT, CSV, ZIP file processing with smart detection
- **👑 Admin Panel**: Complete user management and premium controls
- **⭐ Premium System**: Tiered access with automatic admin privileges
- **🔒 Security**: Safe file handling and input validation

## 🏗️ Architecture

### State-Managed Design
- **UserState Enum**: IDLE, CHANNEL_SETUP, SESSION_UPLOAD, WITHDRAW_PROCESSING, FILE_UPLOAD, ADMIN_COMMAND
- **Conflict Prevention**: No more handler conflicts between different operations
- **Context Persistence**: User data and state maintained across interactions

### Modular Structure
```
📦 RTX Toolkit Bot
├── 🎛️ core/              # Core system components
│   ├── config.py         # Environment configuration
│   ├── database.py       # Async SQLite database
│   └── state_manager.py  # User state management
├── 🎮 handlers/           # Event handlers
│   ├── command_handler.py # Slash commands
│   ├── callback_handler.py # Button interactions
│   └── message_handler.py # Text & file processing
├── 🛠️ utils/             # Utility functions
└── 📊 data/              # Database and logs
```

## ⚙️ Setup

### Prerequisites
- Python 3.8+
- Telegram Bot Token
- Telegram API credentials

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/thertxnetworktwo/toolkit.git
cd toolkit
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Run the bot**
```bash
python main.py
```

## 🔧 Configuration

Create a `.env` file with:

```env
# Bot Configuration
BOT_TOKEN=your_bot_token_here
API_ID=your_api_id
API_HASH=your_api_hash

# Admin Settings
ADMIN_IDS=123456789,987654321

# Database
LOG_LEVEL=INFO
```

## 🎯 Usage

### For Users
1. **Start**: `/start` - Access main menu
2. **Upload**: Send session files or phone number lists
3. **Check**: Use "❄️ Check Frozen" to verify phone status
4. **Manage**: Add channels and manage your account

### For Admins
- **Admin Panel**: Full user management access
- **Premium Control**: Grant/revoke premium access
- **User Statistics**: Monitor bot usage
- **Automatic Privileges**: Auto-premium for admin IDs

## 🛡️ Security Features

- **Input Validation**: All user inputs sanitized and validated
- **State Isolation**: User actions isolated through state management
- **File Safety**: Secure file processing with type validation
- **Admin Protection**: Multi-level admin verification

## 📋 File Support

### Supported Formats
- **📄 TXT Files**: Plain text phone number lists
- **📊 CSV Files**: Comma-separated phone data
- **📦 ZIP Files**: Compressed archives containing session files
- **🔐 Session Files**: Telegram session files (.session)

### Smart Detection
- Automatic file type detection
- Phone number extraction from various formats
- ZIP archive processing with session extraction

## 🔄 State Management

### User States
- **IDLE**: Default state, ready for new actions
- **CHANNEL_SETUP**: Adding new channel configuration
- **SESSION_UPLOAD**: Uploading Telegram session files
- **WITHDRAW_PROCESSING**: Processing withdraw requests
- **FILE_UPLOAD**: Handling file uploads and processing
- **ADMIN_COMMAND**: Admin panel operations

### Benefits
- **No Conflicts**: Eliminates handler interference
- **Better UX**: Clear user flow and expectations
- **Reliability**: Consistent behavior across operations

## 🎨 User Interface

### Professional Icons
- ⚠️ Warnings instead of harsh errors
- 🔙 Friendly navigation buttons  
- 🔒 Clear access control indicators
- ℹ️ Informational messages

### Menu-Driven Design
- Button-based interactions
- Clear action categories
- Intuitive navigation flow

## 📊 Database Schema

### Tables
- **users**: User registration and premium status
- **channels**: User channel configurations
- **sessions**: Stored Telegram session data
- **user_activity**: Activity tracking and analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Powered by [aiosqlite](https://github.com/omnilib/aiosqlite) for async database operations
- Telegram API integration for session management

## 📞 Support

For support and questions:
- 🐛 **Issues**: [GitHub Issues](https://github.com/thertxnetworktwo/toolkit/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/thertxnetworktwo/toolkit/discussions)

---

**⚡ RTX Toolkit Bot - Professional Telegram Number Management** ⚡

### From Old Version
- ❌ **Old**: Text parsing conflicts, handlers fighting
- ✅ **New**: State-managed, clean separation

- ❌ **Old**: Withdraw messages triggering channel setup
- ✅ **New**: Messages only processed in correct state

- ❌ **Old**: Confusing text commands
- ✅ **New**: Clear menu-driven interface

- ❌ **Old**: No user context tracking
- ✅ **New**: Full context awareness

### Professional Features
- ✅ Modern async/await architecture
- ✅ Proper error handling and logging
- ✅ Database with migration support
- ✅ Modular, maintainable code structure
- ✅ Admin panel with full controls
- ✅ Premium user management system

## 📞 Support

For support and questions:
- 🐛 **Issues**: [GitHub Issues](https://github.com/thertxnetworktwo/toolkit/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/thertxnetworktwo/toolkit/discussions)

## 📋 Changelog

### August 27, 2025 - Latest Updates
- 🔧 **Fixed**: Remove Session callback handler - resolves "Unknown action" error
- 🔧 **Fixed**: Entity parsing errors with Unicode filenames (mathematical bold characters)
- ✨ **Enhanced**: Filename sanitization with smart Unicode character mapping
- ✨ **Added**: Complete session management with confirmation dialogs
- 🛡️ **Improved**: Error handling for Telegram entity parsing edge cases

### Initial Release - August 2025
- 🎯 **Complete Rebuild**: Professional state management architecture
- 🎨 **UI Overhaul**: Friendly icons replacing harsh error symbols
- 📁 **File Processing**: Enhanced TXT, CSV, ZIP support with smart detection
- 👑 **Admin System**: Auto-premium privileges and user management
- 🔒 **Security**: Comprehensive data protection and input validation

---

**⚡ RTX Toolkit Bot - Professional Telegram Number Management** ⚡
