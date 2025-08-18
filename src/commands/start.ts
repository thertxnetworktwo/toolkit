import { BotContext } from '../types';
import { logger } from '../utils/logger';

/**
 * Start command handler
 * Welcomes new users and introduces the bot
 */
export const startCommand = async (ctx: BotContext): Promise<void> => {
  try {
    const user = ctx.from;
    const welcomeMessage = `
🚀 *Welcome to RTX Network Toolkit Bot!*

Hello ${user?.first_name || 'there'}! 👋

I'm your dedicated RTX Network assistant, here to help you explore our innovative blockchain toolkit and ecosystem.

🔧 *What I can do:*
• Provide information about RTX Network
• Help with toolkit documentation
• Answer questions about our technology
• Share latest updates and features

🎯 *Quick Start:*
Use /help to see all available commands
Use /about to learn more about RTX Network
Use /ping to check if I'm working properly

Ready to dive into the RTX Network ecosystem? Let's get started! 🌟

*RTX Network - Building the Future of Decentralized Technology*
    `.trim();

    await ctx.replyWithMarkdown(welcomeMessage);
    
    logger.info(`Start command executed for user: ${user?.username || user?.id || 'unknown'}`);
  } catch (error) {
    logger.error('Error in start command:', error);
    await ctx.reply('Sorry, something went wrong. Please try again later.');
  }
};