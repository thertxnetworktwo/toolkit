import { Context } from 'telegraf';
import { logger, formatUptime } from '../utils/helpers.js';

/**
 * Handle the /start command
 * Welcomes new users with RTX Network branding and introduction
 */
export async function handleStart(ctx: Context): Promise<void> {
  try {
    const welcomeMessage = `🚀 *Welcome to RTX Network Toolkit Bot\\!*

Hello ${ctx.from?.first_name || 'there'}\\! I'm your official RTX Network companion bot\\. 

🔧 *What I can do for you:*
• Get information about RTX Network
• Access toolkit features and documentation
• Check bot health and status
• Provide helpful commands and guidance

💡 Type /help to see all available commands and get started\\!

*RTX Network* \\- Powering the future of decentralized connectivity\\.`;

    await ctx.replyWithMarkdownV2(welcomeMessage);
    
    logger.info('Start command executed', {
      userId: ctx.from?.id,
      username: ctx.from?.username,
      firstName: ctx.from?.first_name,
    });
  } catch (error) {
    logger.error('Error handling start command', { error, userId: ctx.from?.id });
    await ctx.reply('Welcome to RTX Network Toolkit Bot! Use /help to see available commands.');
  }
}

/**
 * Handle the /help command
 * Lists all available commands with usage instructions
 */
export async function handleHelp(ctx: Context): Promise<void> {
  try {
    const helpMessage = `📚 *RTX Network Toolkit Bot \\- Help*

*Available Commands:*

🏁 */start*
   Welcome message and bot introduction

❓ */help*
   Display this help message with all commands

ℹ️ */about*
   Learn about RTX Network and this toolkit

🏓 */ping*
   Check bot health and response time

*How to use:*
Simply type any command starting with a forward slash \\(/\\) followed by the command name\\. 

*Need assistance?*
If you encounter any issues or need support, please refer to our documentation or contact the RTX Network team\\.

*RTX Network* \\- Building tomorrow's decentralized infrastructure today\\.`;

    await ctx.replyWithMarkdownV2(helpMessage);
    
    logger.info('Help command executed', {
      userId: ctx.from?.id,
      username: ctx.from?.username,
    });
  } catch (error) {
    logger.error('Error handling help command', { error, userId: ctx.from?.id });
    await ctx.reply('📚 Available commands:\n/start - Welcome message\n/help - Show commands\n/about - RTX Network info\n/ping - Health check');
  }
}

/**
 * Handle the /about command
 * Provides information about RTX Network and the toolkit
 */
export async function handleAbout(ctx: Context): Promise<void> {
  try {
    const aboutMessage = `🌐 *About RTX Network*

*RTX Network* is a cutting\\-edge blockchain platform focused on building robust, scalable, and decentralized infrastructure for the next generation of digital applications\\.

🔧 *RTX Toolkit Features:*
• Comprehensive development tools
• Smart contract deployment utilities
• Network monitoring and analytics
• Community engagement tools
• Real\\-time blockchain insights

🎯 *Our Mission:*
To democratize access to advanced blockchain technology and empower developers to build innovative decentralized solutions\\.

🔗 *Connect with us:*
• Website: [rtxnetwork\\.io](https://rtxnetwork.io)
• Documentation: [docs\\.rtxnetwork\\.io](https://docs.rtxnetwork.io)
• GitHub: [github\\.com/rtxnetwork](https://github.com/rtxnetwork)

*This bot* provides easy access to RTX Network resources and toolkit features directly through Telegram\\.

Built with ❤️ by the RTX Network team\\.`;

    await ctx.replyWithMarkdownV2(aboutMessage);
    
    logger.info('About command executed', {
      userId: ctx.from?.id,
      username: ctx.from?.username,
    });
  } catch (error) {
    logger.error('Error handling about command', { error, userId: ctx.from?.id });
    await ctx.reply('🌐 RTX Network is a cutting-edge blockchain platform building decentralized infrastructure. This bot provides access to toolkit features and network information.');
  }
}

/**
 * Handle the /ping command
 * Provides health check and bot status information
 */
export async function handlePing(ctx: Context): Promise<void> {
  try {
    const startTime = Date.now();
    const uptimeSeconds = process.uptime();
    const formattedUptime = formatUptime(uptimeSeconds);
    
    // Send initial response
    const message = await ctx.reply('🏓 Pinging...');
    
    // Calculate response time
    const responseTime = Date.now() - startTime;
    
    const pingMessage = `🏓 *Pong\\!*

✅ *Bot Status:* Online and healthy
⚡ *Response Time:* ${responseTime}ms
⏱️ *Uptime:* ${formattedUptime}
🤖 *Version:* 1\\.0\\.0
🔄 *Node\\.js:* ${process.version}

*All systems operational\\!*`;

    // Edit the message with the ping results
    await ctx.telegram.editMessageText(
      message.chat.id,
      message.message_id,
      undefined,
      pingMessage,
      { parse_mode: 'MarkdownV2' }
    );
    
    logger.info('Ping command executed', {
      userId: ctx.from?.id,
      username: ctx.from?.username,
      responseTime,
      uptime: formattedUptime,
    });
  } catch (error) {
    logger.error('Error handling ping command', { error, userId: ctx.from?.id });
    await ctx.reply('🏓 Pong! Bot is online and responding.');
  }
}