import dotenv from 'dotenv';
import { AppConfig } from '../types';

// Load environment variables
dotenv.config();

/**
 * Validates that required environment variables are set
 */
function validateEnvironment(): void {
  const requiredVars = ['BOT_TOKEN'];
  const missingVars = requiredVars.filter(varName => !process.env[varName]);
  
  if (missingVars.length > 0) {
    throw new Error(`Missing required environment variables: ${missingVars.join(', ')}`);
  }
}

/**
 * Application configuration
 */
export const config: AppConfig = {
  bot: {
    token: process.env.BOT_TOKEN || '',
    name: process.env.BOT_NAME || 'RTX Toolkit Bot',
    username: process.env.BOT_USERNAME || 'rtx_toolkit_bot',
    port: parseInt(process.env.PORT || '3000', 10),
    nodeEnv: process.env.NODE_ENV || 'development'
  },
  log: {
    level: process.env.LOG_LEVEL || 'info',
    file: process.env.LOG_FILE || 'logs/bot.log'
  }
};

// Validate environment on import
validateEnvironment();

export default config;