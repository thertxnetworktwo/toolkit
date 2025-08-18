import { BotContext } from '../types';
import { logger } from '../utils/logger';

/**
 * Ping command handler
 * Health check command to verify bot functionality
 */
export const pingCommand = async (ctx: BotContext): Promise<void> => {
  try {
    const startTime = Date.now();
    
    // Calculate uptime
    const uptimeSeconds = process.uptime();
    const uptimeMinutes = Math.floor(uptimeSeconds / 60);
    const uptimeHours = Math.floor(uptimeMinutes / 60);
    const uptimeDays = Math.floor(uptimeHours / 24);
    
    let uptimeString = '';
    if (uptimeDays > 0) {
      uptimeString += `${uptimeDays}d `;
    }
    if (uptimeHours % 24 > 0) {
      uptimeString += `${uptimeHours % 24}h `;
    }
    if (uptimeMinutes % 60 > 0) {
      uptimeString += `${uptimeMinutes % 60}m `;
    }
    uptimeString += `${Math.floor(uptimeSeconds % 60)}s`;

    const pingMessage = `
🏓 *Pong!*

✅ *Bot Status:* Healthy and responsive
⏱️ *Response Time:* ${Date.now() - startTime}ms
⏰ *Uptime:* ${uptimeString}
🕐 *Current Time:* ${new Date().toLocaleString()}
🤖 *Bot Version:* 1.0.0
⚡ *Node.js Version:* ${process.version}
🔧 *Environment:* ${process.env.NODE_ENV || 'development'}

All systems operational! 🚀
    `.trim();

    await ctx.replyWithMarkdown(pingMessage);
    
    logger.info(`Ping command executed for user: ${ctx.from?.username || ctx.from?.id || 'unknown'}, response time: ${Date.now() - startTime}ms`);
  } catch (error) {
    logger.error('Error in ping command:', error);
    await ctx.reply('🔴 Pong! (with errors - check logs)');
  }
};