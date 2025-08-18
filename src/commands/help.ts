import { BotContext } from '../types';
import { logger } from '../utils/logger';

/**
 * Help command handler
 * Lists all available commands and their descriptions
 */
export const helpCommand = async (ctx: BotContext): Promise<void> => {
  try {
    const helpMessage = `
🤖 *RTX Network Toolkit Bot - Help*

Here are all the commands I understand:

📋 *Available Commands:*

🚀 */start* - Welcome message and bot introduction
❓ */help* - Show this help message
ℹ️ */about* - Learn about RTX Network and our toolkit
🏓 */ping* - Check bot status and response time

💡 *Tips:*
• All commands work in private chats
• Commands are case-insensitive
• Feel free to ask if you need assistance!

🔗 *Useful Links:*
• RTX Network Website: [Coming Soon]
• Documentation: [Coming Soon]
• GitHub Repository: [Coming Soon]

Need more help? Just type your question and I'll do my best to assist you!

*RTX Network - Empowering Decentralized Innovation* 🌐
    `.trim();

    await ctx.replyWithMarkdown(helpMessage);
    
    logger.info(`Help command executed for user: ${ctx.from?.username || ctx.from?.id || 'unknown'}`);
  } catch (error) {
    logger.error('Error in help command:', error);
    await ctx.reply('Sorry, I couldn\'t display the help information. Please try again later.');
  }
};