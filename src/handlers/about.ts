import { Context } from 'telegraf';
import logger from '../utils/logger';

export const aboutHandler = async (ctx: Context): Promise<void> => {
  try {
    const message = `
ℹ️ *About RTX Toolkit*

*Version:* 1.0.0
*Created by:* RTX Network
*Built with:* Node.js, TypeScript, and Telegraf

*Description:*
RTX Toolkit is a powerful Telegram bot designed to provide essential tools and utilities for the RTX Network community. Built with modern technologies and best practices, it offers a reliable and efficient user experience.

*Key Features:*
• 🚀 Fast and responsive command processing
• 🔧 Modular and extensible architecture
• 📊 Comprehensive logging and monitoring
• 🐳 Docker containerization for easy deployment
• 🔄 Continuous integration and deployment
• 🛡️ Error handling and recovery

*Technology Stack:*
• **Runtime:** Node.js (v18+)
• **Language:** TypeScript
• **Bot Framework:** Telegraf
• **Logging:** Winston
• **Containerization:** Docker
• **CI/CD:** GitHub Actions

*Open Source:*
This bot is part of the RTX Network ecosystem and follows modern development practices including proper typing, error handling, and automated deployment.

For more information, visit our GitHub repository or contact our team.

Made with ❤️ by RTX Network
    `.trim();

    await ctx.replyWithMarkdown(message);
    logger.info(`About command executed by user: ${ctx.from?.username || ctx.from?.id}`);
  } catch (error) {
    logger.error('Error in about handler:', error);
    await ctx.reply('Sorry, something went wrong. Please try again later.');
  }
};