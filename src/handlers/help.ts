import { Context } from 'telegraf';
import logger from '../utils/logger';

export const helpHandler = async (ctx: Context): Promise<void> => {
  try {
    const message = `
🛠️ *RTX Toolkit Bot - Help*

*Available Commands:*

🔸 /start - Welcome message and quick start guide
🔸 /help - Show this help message
🔸 /about - Information about RTX Toolkit

*How to use:*
Simply type any of the commands above to interact with the bot.

*Need more help?*
If you encounter any issues or need additional assistance, please contact our support team.

*Bot Features:*
• Real-time command processing
• Error handling and logging
• Clean and intuitive interface
• Regular updates and improvements

Thank you for using RTX Toolkit! 🚀
    `.trim();

    await ctx.replyWithMarkdown(message);
    logger.info(`Help command executed by user: ${ctx.from?.username || ctx.from?.id}`);
  } catch (error) {
    logger.error('Error in help handler:', error);
    await ctx.reply('Sorry, something went wrong. Please try again later.');
  }
};