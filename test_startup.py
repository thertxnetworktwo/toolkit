"""
Quick bot startup test
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_bot_startup():
    """Test bot can initialize without starting polling"""
    print("🚀 Testing RTX Toolkit Bot Startup...")
    
    try:
        from core.config import Config
        from core.database import DatabaseManager
        from core.state_manager import StateManager
        from utils.logger import setup_logging
        
        # Setup logging
        setup_logging()
        print("✅ Logging configured")
        
        # Test configuration
        config = Config()
        print(f"✅ Configuration loaded - Bot token ending: ...{config.bot_token[-10:]}")
        print(f"✅ Admin ID configured: {config.admin_ids[0]}")
        print(f"✅ API credentials loaded")
        
        # Test database
        db = DatabaseManager()
        await db.initialize()
        print("✅ Database initialized")
        
        # Test state manager
        state_manager = StateManager()
        print("✅ State manager ready")
        
        # Import main bot class
        from main import RTXToolkitBot
        
        # Initialize bot (without starting)
        bot = RTXToolkitBot()
        print("✅ Bot application created")
        
        # Setup handlers
        bot.setup_handlers()
        print("✅ All handlers registered")
        
        # Initialize bot application
        await bot.application.initialize()
        print("✅ Bot application initialized")
        
        # Get bot info
        bot_info = await bot.application.bot.get_me()
        print(f"✅ Bot connected: @{bot_info.username}")
        print(f"✅ Bot name: {bot_info.first_name}")
        
        # Cleanup
        await bot.cleanup()
        
        print("\n🎉 RTX Toolkit Bot Startup Test PASSED!")
        print(f"\n🤖 Your bot @{bot_info.username} is ready to run!")
        print("\n📝 To start the bot:")
        print("   python main.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_bot_startup())
