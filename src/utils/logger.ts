import winston from 'winston';
import { config } from '../config/config';
import { Logger } from '../types';

/**
 * Create logs directory if it doesn't exist
 */
const createLogsDirectory = (): void => {
  const fs = require('fs');
  const path = require('path');
  const logDir = path.dirname(config.log.file);
  
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
};

/**
 * Configure Winston logger
 */
const createLogger = (): winston.Logger => {
  createLogsDirectory();

  const logFormat = winston.format.combine(
    winston.format.timestamp({
      format: 'YYYY-MM-DD HH:mm:ss'
    }),
    winston.format.errors({ stack: true }),
    winston.format.json(),
    winston.format.printf(({ timestamp, level, message, stack }) => {
      return `${timestamp} [${level.toUpperCase()}]: ${message}${stack ? '\n' + stack : ''}`;
    })
  );

  return winston.createLogger({
    level: config.log.level,
    format: logFormat,
    transports: [
      // Write to file
      new winston.transports.File({
        filename: config.log.file,
        maxsize: 5242880, // 5MB
        maxFiles: 5,
      }),
      // Write to console in development
      ...(config.bot.nodeEnv === 'development' ? [
        new winston.transports.Console({
          format: winston.format.combine(
            winston.format.colorize(),
            winston.format.simple()
          )
        })
      ] : [])
    ],
    exceptionHandlers: [
      new winston.transports.File({ filename: 'logs/exceptions.log' })
    ],
    rejectionHandlers: [
      new winston.transports.File({ filename: 'logs/rejections.log' })
    ]
  });
};

/**
 * Logger instance
 */
export const logger: Logger = createLogger();

export default logger;