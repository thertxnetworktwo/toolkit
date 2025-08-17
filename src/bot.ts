import { Telegraf, Context } from 'telegraf';
import config from './config';
import logger from './utils/logger';
import { startHandler, helpHandler, aboutHandler } from './handlers';
import fs from 'fs';
import path from 'path';

// Ensure logs directory exists
const logsDir = path.join(process.cwd(), 'logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

// Create bot instance
const bot = new Telegraf(config.botToken);

// Error handling middleware
bot.catch((err: any, ctx: Context) => {
  logger.error(`Bot error for ${ctx.updateType}:`, err);
  ctx.reply('An unexpected error occurred. Please try again later.').catch((replyErr) => {
    logger.error('Failed to send error reply:', replyErr);
  });
});

// Command handlers
bot.start(startHandler);
bot.help(helpHandler);
bot.command('about', aboutHandler);

// Handle unknown commands
bot.on('message', async (ctx) => {
  const messageText = 'text' in ctx.message ? ctx.message.text : '';
  
  if (messageText?.startsWith('/')) {
    await ctx.reply(
      'Unknown command. Use /help to see available commands.',
      { 
        reply_parameters: { 
          message_id: ctx.message.message_id 
        }
      }
    );
    logger.warn(`Unknown command received: ${messageText} from user: ${ctx.from?.id}`);
  }
});

// Bot startup
const startBot = async (): Promise<void> => {
  try {
    // Enable graceful stop
    process.once('SIGINT', () => bot.stop('SIGINT'));
    process.once('SIGTERM', () => bot.stop('SIGTERM'));

    // Start bot
    await bot.launch();
    logger.info('🚀 RTX Toolkit Bot started successfully!');
    logger.info(`Bot username: @${bot.botInfo?.username}`);
    logger.info(`Environment: ${config.environment}`);
    
    // Health check endpoint (for Docker health checks)
    if (config.environment === 'production') {
      const http = require('http');
      const server = http.createServer((_req: any, res: any) => {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('RTX Toolkit Bot is running');
      });
      
      server.listen(config.port, () => {
        logger.info(`Health check server listening on port ${config.port}`);
      });
    }
    
  } catch (error) {
    logger.error('Failed to start bot:', error);
    process.exit(1);
  }
};

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception:', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Start the bot
startBot();