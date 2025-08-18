import 'dotenv/config';
import { Telegraf, Context } from 'telegraf';
import { logger, validateEnvironment } from './utils/helpers.js';
import { handleStart, handleHelp, handleAbout, handlePing } from './commands/index.js';

/**
 * RTX Network Toolkit Telegram Bot
 * A comprehensive bot providing access to RTX Network tools and information
 */
class RTXToolkitBot {
  private bot: Telegraf;
  private readonly startTime: Date;

  constructor(token: string) {
    this.bot = new Telegraf(token);
    this.startTime = new Date();
    this.setupMiddleware();
    this.setupCommands();
    this.setupErrorHandling();
  }

  /**
   * Set up middleware for logging and error handling
   */
  private setupMiddleware(): void {
    // Logging middleware
    this.bot.use(async (ctx: Context, next) => {
      const startTime = Date.now();
      
      logger.info('Incoming update', {
        updateId: ctx.update.update_id,
        chatId: ctx.chat?.id,
        userId: ctx.from?.id,
        username: ctx.from?.username,
        messageType: 'message' in ctx.update ? 'message' : 'other',
      });

      try {
        await next();
        const duration = Date.now() - startTime;
        logger.info('Update processed successfully', {
          updateId: ctx.update.update_id,
          duration: `${duration}ms`,
        });
      } catch (error) {
        const duration = Date.now() - startTime;
        logger.error('Error processing update', {
          updateId: ctx.update.update_id,
          duration: `${duration}ms`,
          error: error instanceof Error ? error.message : 'Unknown error',
        });
        throw error;
      }
    });

    // Rate limiting and security middleware
    this.bot.use(async (_ctx: Context, next) => {
      // Basic rate limiting logic could go here
      // For now, we'll just pass through
      await next();
    });
  }

  /**
   * Set up bot commands
   */
  private setupCommands(): void {
    // Command handlers
    this.bot.command('start', handleStart);
    this.bot.command('help', handleHelp);
    this.bot.command('about', handleAbout);
    this.bot.command('ping', handlePing);

    // Handle unknown commands
    this.bot.on('message', async (ctx: Context) => {
      if (ctx.message && 'text' in ctx.message && ctx.message.text.startsWith('/')) {
        const command = ctx.message.text.split(' ')[0];
        
        logger.info('Unknown command received', {
          command,
          userId: ctx.from?.id,
          username: ctx.from?.username,
        });

        await ctx.reply(
          `❓ Unknown command: ${command}\n\n` +
          'Use /help to see available commands or /start for a welcome message.'
        );
      }
    });
  }

  /**
   * Set up global error handling
   */
  private setupErrorHandling(): void {
    this.bot.catch(async (err: any, ctx: Context) => {
      logger.error('Bot error occurred', {
        error: err.message || 'Unknown error',
        stack: err.stack,
        updateId: ctx.update.update_id,
        userId: ctx.from?.id,
      });

      try {
        await ctx.reply(
          '⚠️ An error occurred while processing your request. Please try again later.\n\n' +
          'If the problem persists, use /help for available commands.'
        );
      } catch (replyError) {
        logger.error('Failed to send error message to user', {
          originalError: err.message,
          replyError: replyError instanceof Error ? replyError.message : 'Unknown error',
          userId: ctx.from?.id,
        });
      }
    });

    // Handle process errors
    process.on('uncaughtException', (error) => {
      logger.error('Uncaught exception', { error: error.message, stack: error.stack });
      this.gracefulShutdown();
    });

    process.on('unhandledRejection', (reason, promise) => {
      logger.error('Unhandled rejection', { reason, promise });
    });

    // Handle shutdown signals
    process.on('SIGINT', () => {
      logger.info('Received SIGINT, shutting down gracefully');
      this.gracefulShutdown();
    });

    process.on('SIGTERM', () => {
      logger.info('Received SIGTERM, shutting down gracefully');
      this.gracefulShutdown();
    });
  }

  /**
   * Start the bot
   */
  public async start(): Promise<void> {
    try {
      logger.info('Starting RTX Toolkit Bot...', {
        nodeVersion: process.version,
        environment: process.env.NODE_ENV || 'development',
        logLevel: logger.level,
      });

      if (process.env.NODE_ENV === 'production' && process.env.WEBHOOK_URL) {
        // Use webhooks in production
        const webhookUrl = process.env.WEBHOOK_URL;
        const port = parseInt(process.env.WEBHOOK_PORT || '8443', 10);
        const secretToken = process.env.WEBHOOK_SECRET_TOKEN;
        
        await this.bot.launch({
          webhook: {
            domain: webhookUrl,
            port,
            ...(secretToken && { secretToken }),
          },
        });
        
        logger.info('Bot started with webhook', { webhookUrl, port });
      } else {
        // Use long polling for development
        await this.bot.launch();
        logger.info('Bot started with long polling');
      }

      logger.info('RTX Toolkit Bot is running!', {
        botUsername: this.bot.botInfo?.username,
        startTime: this.startTime.toISOString(),
      });
    } catch (error) {
      logger.error('Failed to start bot', {
        error: error instanceof Error ? error.message : 'Unknown error',
      });
      process.exit(1);
    }
  }

  /**
   * Gracefully shutdown the bot
   */
  private gracefulShutdown(): void {
    logger.info('Initiating graceful shutdown...');
    
    this.bot.stop('SIGTERM');
    
    setTimeout(() => {
      logger.error('Force shutdown after timeout');
      process.exit(1);
    }, 5000);
    
    logger.info('Bot shutdown complete');
    process.exit(0);
  }
}

/**
 * Main function to initialize and start the bot
 */
async function main(): Promise<void> {
  try {
    // Validate environment variables
    validateEnvironment();
    
    // Get bot token
    const botToken = process.env.BOT_TOKEN!;
    
    // Create and start bot
    const bot = new RTXToolkitBot(botToken);
    await bot.start();
  } catch (error) {
    logger.error('Failed to initialize bot', {
      error: error instanceof Error ? error.message : 'Unknown error',
    });
    process.exit(1);
  }
}

// Start the bot
if (require.main === module) {
  main().catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

export { RTXToolkitBot };