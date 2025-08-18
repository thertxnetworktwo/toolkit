import { BotContext } from '../types';
import { logger } from '../utils/logger';

/**
 * About command handler
 * Provides information about RTX Network and the toolkit
 */
export const aboutCommand = async (ctx: BotContext): Promise<void> => {
  try {
    const aboutMessage = `
🌟 *About RTX Network*

*RTX Network* is a cutting-edge blockchain ecosystem focused on building the next generation of decentralized applications and infrastructure.

🔧 *RTX Toolkit:*
Our comprehensive development toolkit provides:
• Smart contract templates and utilities
• Development frameworks and libraries  
• Testing and deployment tools
• Security audit resources
• Documentation and guides

🎯 *Our Mission:*
To democratize blockchain development by providing powerful, user-friendly tools that enable developers to build secure, scalable, and innovative decentralized applications.

🚀 *Key Features:*
• Professional-grade development tools
• Enterprise security standards
• Comprehensive documentation
• Active community support
• Regular updates and improvements

💎 *Technology Stack:*
• Built with modern TypeScript/Node.js
• Telegram Bot API integration
• Docker containerization
• CI/CD automation
• Production-ready monitoring

🤝 *Community:*
Join our growing community of developers, innovators, and blockchain enthusiasts working together to shape the future of decentralized technology.

*Version:* 1.0.0
*Bot Status:* ✅ Active
*Last Updated:* ${new Date().toISOString().split('T')[0]}

*RTX Network - Where Innovation Meets Blockchain* 🚀
    `.trim();

    await ctx.replyWithMarkdown(aboutMessage);
    
    logger.info(`About command executed for user: ${ctx.from?.username || ctx.from?.id || 'unknown'}`);
  } catch (error) {
    logger.error('Error in about command:', error);
    await ctx.reply('Sorry, I couldn\'t display the about information. Please try again later.');
  }
};