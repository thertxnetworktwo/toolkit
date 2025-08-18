import { Telegraf } from 'telegraf';
import { BotContext } from './types';
import { config } from './config/config';
import { logger } from './utils/logger';
import { startCommand } from './commands/start';
import { helpCommand } from './commands/help';
import { aboutCommand } from './commands/about';
import { pingCommand } from './commands/ping';

/**
 * RTX Network Toolkit Telegram Bot
 * A professional bot representing the RTX Network brand
 */
class RTXToolkitBot {
  private bot: Telegraf<BotContext>;
  private readonly startTime: Date;

  constructor() {
    this.startTime = new Date();
    this.bot = new Telegraf<BotContext>(config.bot.token);
    this.setupMiddleware();
    this.setupCommands();
    this.setupErrorHandling();
  }

  /**
   * Setup middleware for logging and error handling
   */
  private setupMiddleware(): void {
    // Logging middleware
    this.bot.use(async (ctx, next) => {
      const start = Date.now();
      const user = ctx.from;
      
      logger.info(`Incoming update from ${user?.username || user?.id || 'unknown'}: ${ctx.updateType}`);
      
      try {
        await next();
        const responseTime = Date.now() - start;
        logger.info(`Request processed in ${responseTime}ms`);
      } catch (error) {
        const responseTime = Date.now() - start;
        logger.error(`Request failed in ${responseTime}ms:`, error);
        throw error;
      }
    });
  }

  /**
   * Setup bot commands
   */
  private setupCommands(): void {
    // Command handlers
    this.bot.command('start', startCommand);
    this.bot.command('help', helpCommand);
    this.bot.command('about', aboutCommand);
    this.bot.command('ping', pingCommand);

    // Handle unknown commands
    this.bot.on('text', async (ctx) => {
      const text = ctx.message.text;
      
      // Check if it's a command that starts with /
      if (text.startsWith('/')) {
        await ctx.reply(
          `🤔 Unknown command: ${text}\n\n` +
          `Use /help to see all available commands.`
        );
        logger.warn(`Unknown command received: ${text} from user: ${ctx.from?.username || ctx.from?.id}`);
      } else {
        // Handle regular messages
        await ctx.reply(
          `👋 Hello! I'm the RTX Network Toolkit Bot.\n\n` +
          `I respond to commands. Use /help to see what I can do!`
        );
        logger.info(`Regular message received from user: ${ctx.from?.username || ctx.from?.id}`);
      }
    });

    // Handle other message types
    this.bot.on('sticker', async (ctx) => {
      await ctx.reply('Nice sticker! 😄 Use /help to see my commands.');
    });

    this.bot.on('photo', async (ctx) => {
      await ctx.reply('Great photo! 📸 Use /help to see my commands.');
    });
  }

  /**
   * Setup error handling
   */
  private setupErrorHandling(): void {
    this.bot.catch((error, ctx) => {
      logger.error('Bot error occurred:', error);
      
      // Try to send error message to user
      ctx.reply('😔 Sorry, an error occurred. Please try again later.')
        .catch(replyError => {
          logger.error('Failed to send error message to user:', replyError);
        });
    });

    // Handle process errors
    process.on('uncaughtException', (error) => {
      logger.error('Uncaught Exception:', error);
      this.gracefulShutdown();
    });

    process.on('unhandledRejection', (reason) => {
      logger.error('Unhandled Rejection:', reason);
      this.gracefulShutdown();
    });

    // Handle shutdown signals
    process.on('SIGINT', () => {
      logger.info('Received SIGINT signal');
      this.gracefulShutdown();
    });

    process.on('SIGTERM', () => {
      logger.info('Received SIGTERM signal');
      this.gracefulShutdown();
    });
  }

  /**
   * Start the bot
   */
  public async start(): Promise<void> {
    try {
      logger.info('Starting RTX Network Toolkit Bot...');
      
      // Get bot info
      const botInfo = await this.bot.telegram.getMe();
      logger.info(`Bot started successfully: @${botInfo.username} (${botInfo.first_name})`);

      // Set bot commands for better UX
      await this.bot.telegram.setMyCommands([
        { command: 'start', description: 'Welcome message and introduction' },
        { command: 'help', description: 'Show all available commands' },
        { command: 'about', description: 'Learn about RTX Network' },
        { command: 'ping', description: 'Check bot status' }
      ]);

      // Start polling
      await this.bot.launch();
      
      logger.info(`Bot is now running and listening for updates...`);
      logger.info(`Startup time: ${new Date().toISOString()}`);
      
    } catch (error) {
      logger.error('Failed to start bot:', error);
      process.exit(1);
    }
  }

  /**
   * Graceful shutdown
   */
  private async gracefulShutdown(): Promise<void> {
    logger.info('Initiating graceful shutdown...');
    
    try {
      await this.bot.stop('SIGTERM');
      const uptime = Date.now() - this.startTime.getTime();
      logger.info(`Bot stopped gracefully. Uptime: ${Math.floor(uptime / 1000)}s`);
      process.exit(0);
    } catch (error) {
      logger.error('Error during shutdown:', error);
      process.exit(1);
    }
  }

  /**
   * Get bot uptime
   */
  public getUptime(): number {
    return Math.floor((Date.now() - this.startTime.getTime()) / 1000);
  }
}

// Initialize and start the bot
const bot = new RTXToolkitBot();
bot.start().catch((error) => {
  logger.error('Failed to initialize bot:', error);
  process.exit(1);
});

export default RTXToolkitBot;