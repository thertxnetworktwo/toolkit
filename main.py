"""
RTX Toolkit Bot - Professional State-Managed Architecture
A Telegram bot for checking frozen phone numbers with proper state management
"""

import asyncio
import logging
import sys
from pathlib import Path
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.config import Config
from core.database import DatabaseManager
from core.state_manager import StateManager
from handlers.command_handler import CommandHandler as CmdHandler
from handlers.callback_handler import CallbackHandler
from handlers.message_handler import MessageHandler as MsgHandler
from utils.logger import setup_logging

class RTXToolkitBot:
    """
    Main bot application with professional state management
    """
    
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager()
        self.state_manager = StateManager()
        self.logger = logging.getLogger(__name__)
        
        # Initialize bot application
        self.application = Application.builder().token(self.config.bot_token).build()
        
        # Initialize handlers
        self.cmd_handler = CmdHandler(self.db, self.state_manager)
        self.callback_handler = CallbackHandler(self.db, self.state_manager)
        self.msg_handler = MsgHandler(self.db, self.state_manager)
        
    def setup_handlers(self):
        """Setup all bot handlers with proper order"""
        
        # Command handlers (highest priority)
        self.application.add_handler(CommandHandler("start", self.cmd_handler.start_command))
        self.application.add_handler(CommandHandler("help", self.cmd_handler.help_command))
        self.application.add_handler(CommandHandler("admin", self.cmd_handler.admin_command))
        self.application.add_handler(CommandHandler("status", self.cmd_handler.status_command))
        
        # Callback query handler (menu interactions)
        self.application.add_handler(CallbackQueryHandler(self.callback_handler.handle_callback))
        
        # Document handler (file uploads)
        self.application.add_handler(MessageHandler(
            filters.Document.ALL, 
            self.msg_handler.handle_document
        ))
        
        # Text message handler (state-based, lowest priority)
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            self.msg_handler.handle_text
        ))
        
        # Error handler
        self.application.add_error_handler(self._error_handler)
        
        self.logger.info("All handlers registered successfully")
    
    async def _error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        self.logger.error(f"Update {update} caused error {context.error}")
        
        # If the error was caused by a user interaction, inform them
        if update and update.effective_user:
            try:
                await context.bot.send_message(
                    chat_id=update.effective_user.id,
                    text="⚠️ An error occurred while processing your request. Please try again."
                )
            except Exception as e:
                self.logger.error(f"Failed to send error message to user: {e}")
    
    async def start(self):
        """Start the bot"""
        try:
            # Initialize database
            await self.db.initialize()
            self.logger.info("Database initialized")
            
            # Setup handlers
            self.setup_handlers()
            
            # Start bot
            await self.application.initialize()
            await self.application.start()
            
            self.logger.info("RTX Toolkit Bot started successfully")
            self.logger.info(f"Bot username: @{self.application.bot.username}")
            
            # Start polling
            await self.application.updater.start_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES
            )
            
            # Keep the bot running using asyncio.Event
            stop_event = asyncio.Event()
            
            # Add signal handlers for graceful shutdown
            import signal
            def signal_handler(signum, frame):
                self.logger.info(f"Received signal {signum}, stopping bot...")
                stop_event.set()
            
            for sig in [signal.SIGINT, signal.SIGTERM]:
                try:
                    signal.signal(sig, signal_handler)
                except (OSError, ValueError):
                    # Windows doesn't support all signals
                    pass
            
            self.logger.info("Bot is running... Press Ctrl+C to stop")
            await stop_event.wait()
            
        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt, shutting down...")
        except Exception as e:
            self.logger.error(f"Failed to start bot: {e}")
            raise
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Cleanup resources gracefully"""
        self.logger.info("Starting cleanup process...")
        try:
            # Stop the updater first with timeout
            if hasattr(self, 'application') and self.application.updater.running:
                self.logger.info("Stopping updater...")
                try:
                    await asyncio.wait_for(self.application.updater.stop(), timeout=5.0)
                except asyncio.TimeoutError:
                    self.logger.warning("Updater stop timed out")
                    
            # Then stop the application with timeout
            if hasattr(self, 'application') and self.application.running:
                self.logger.info("Stopping application...")
                try:
                    await asyncio.wait_for(self.application.stop(), timeout=5.0)
                except asyncio.TimeoutError:
                    self.logger.warning("Application stop timed out")
                    
            # Finally shutdown with timeout
            if hasattr(self, 'application'):
                self.logger.info("Shutting down application...")
                try:
                    await asyncio.wait_for(self.application.shutdown(), timeout=5.0)
                except asyncio.TimeoutError:
                    self.logger.warning("Application shutdown timed out")
            
            # Close database
            if hasattr(self, 'db'):
                self.logger.info("Closing database...")
                await self.db.close()
                
            self.logger.info("Bot cleanup completed successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
            # Don't re-raise during cleanup

async def main():
    """Main entry point"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting RTX Toolkit Bot...")
        bot = RTXToolkitBot()
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
