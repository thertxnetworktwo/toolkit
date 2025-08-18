import { Context } from 'telegraf';

/**
 * Bot configuration interface
 */
export interface BotConfig {
  token: string;
  name: string;
  username: string;
  port: number;
  nodeEnv: string;
}

/**
 * Logging configuration interface
 */
export interface LogConfig {
  level: string;
  file: string;
}

/**
 * Application configuration interface
 */
export interface AppConfig {
  bot: BotConfig;
  log: LogConfig;
}

/**
 * Extended Telegram context with additional properties
 */
export interface BotContext extends Context {
  // Add any custom context properties here if needed
}

/**
 * Command handler function type
 */
export type CommandHandler = (ctx: BotContext) => Promise<void> | void;

/**
 * Bot command interface
 */
export interface BotCommand {
  command: string;
  description: string;
  handler: CommandHandler;
}

/**
 * Logger interface
 */
export interface Logger {
  info(message: string, meta?: any): void;
  warn(message: string, meta?: any): void;
  error(message: string, meta?: any): void;
  debug(message: string, meta?: any): void;
}

/**
 * Health check status
 */
export interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  timestamp: string;
  uptime: number;
  version: string;
}