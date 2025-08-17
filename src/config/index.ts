import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

export interface Config {
  botToken: string;
  logLevel: string;
  environment: string;
  port: number;
}

const config: Config = {
  botToken: process.env.BOT_TOKEN || '',
  logLevel: process.env.LOG_LEVEL || 'info',
  environment: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3000', 10),
};

// Validate required configuration
if (!config.botToken) {
  throw new Error('BOT_TOKEN environment variable is required');
}

export default config;