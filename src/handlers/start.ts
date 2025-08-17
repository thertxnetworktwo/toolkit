import { Context } from 'telegraf';
import logger from '../utils/logger';

export const startHandler = async (ctx: Context): Promise<void> => {
  try {
    const username = ctx.from?.username || ctx.from?.first_name || 'User';
    
    const message = `
🚀 *Welcome to RTX Toolkit!*

Hello ${username}! I'm your RTX Toolkit bot, ready to assist you.

*Available Commands:*
/start - Show this welcome message
/help - Get help and command list
/about - Learn more about RTX Toolkit

Let's get started! Use /help to see what I can do for you.
    `.trim();

    await ctx.replyWithMarkdown(message);
    logger.info(`Start command executed by user: ${username} (ID: ${ctx.from?.id})`);
  } catch (error) {
    logger.error('Error in start handler:', error);
    await ctx.reply('Sorry, something went wrong. Please try again later.');
  }
};