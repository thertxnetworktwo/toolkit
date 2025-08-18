# RTX Network Toolkit Bot 🤖

[![Build Status](https://github.com/thertxnetworktwo/toolkit/workflows/Build%20and%20Deploy%20RTX%20Toolkit%20Bot/badge.svg)](https://github.com/thertxnetworktwo/toolkit/actions)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://hub.docker.com)
[![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Node.js](https://img.shields.io/badge/node.js-18+-brightgreen.svg?style=flat&logo=node.js)](https://nodejs.org)

A professional Telegram bot representing the RTX Network brand, built with TypeScript and modern development practices.

## 🚀 Features

- **🤖 Professional Bot Interface**: Clean, branded Telegram bot experience
- **⚡ TypeScript**: Full type safety and modern JavaScript features
- **🔧 Command System**: Modular command handlers for extensibility
- **📊 Logging**: Comprehensive logging with Winston
- **🐳 Docker Ready**: Production-ready containerization
- **🔄 CI/CD**: Automated deployment with GitHub Actions
- **🛡️ Security**: Environment variable validation and secure practices
- **📚 Documentation**: Comprehensive setup and usage guides

## 📋 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and bot introduction |
| `/help` | List all available commands |
| `/about` | Information about RTX Network and toolkit |
| `/ping` | Health check and bot status |

## 🛠️ Quick Start

### Prerequisites

- Node.js 18 or higher
- npm or yarn
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/thertxnetworktwo/toolkit.git
   cd toolkit
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Setup environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your BOT_TOKEN
   ```

4. **Build and start in development mode:**
   ```bash
   npm run dev
   ```

5. **Build for production:**
   ```bash
   npm run build
   npm start
   ```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Clone and configure:**
   ```bash
   git clone https://github.com/thertxnetworktwo/toolkit.git
   cd toolkit
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f rtx-toolkit-bot
   ```

### Manual Docker Build

```bash
# Build the image
docker build -t rtx-toolkit-bot .

# Run the container
docker run -d \
  --name rtx-toolkit-bot \
  --restart unless-stopped \
  -e BOT_TOKEN=your_bot_token_here \
  -e NODE_ENV=production \
  -v $(pwd)/logs:/app/logs \
  rtx-toolkit-bot
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BOT_TOKEN` | Telegram Bot Token from @BotFather | ✅ | - |
| `BOT_NAME` | Display name for the bot | ❌ | RTX Toolkit Bot |
| `BOT_USERNAME` | Bot username | ❌ | rtx_toolkit_bot |
| `LOG_LEVEL` | Logging level (error, warn, info, debug) | ❌ | info |
| `LOG_FILE` | Path to log file | ❌ | logs/bot.log |
| `PORT` | Port for health checks | ❌ | 3000 |
| `NODE_ENV` | Environment (development/production) | ❌ | production |

### Getting a Bot Token

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` command
3. Follow the prompts to create your bot
4. Copy the provided token to your `.env` file

## 🏗️ Project Structure

```
├── src/
│   ├── bot.ts              # Main bot application
│   ├── commands/           # Command handlers
│   │   ├── start.ts        # Welcome command
│   │   ├── help.ts         # Help command
│   │   ├── about.ts        # About command
│   │   └── ping.ts         # Health check command
│   ├── config/             # Configuration management
│   │   └── config.ts       # Environment configuration
│   ├── utils/              # Utility functions
│   │   └── logger.ts       # Winston logger setup
│   └── types/              # TypeScript type definitions
│       └── index.ts        # Shared interfaces
├── .github/workflows/      # GitHub Actions CI/CD
├── logs/                   # Application logs
├── package.json            # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # This file
```

## 🔧 Development

### Available Scripts

```bash
npm run dev        # Start in development mode with hot reload
npm run build      # Build TypeScript to JavaScript
npm start          # Start production server
npm run lint       # Run ESLint
npm run lint:fix   # Fix ESLint issues automatically
npm run clean      # Remove build artifacts
```

### Code Style

This project uses:
- **ESLint** for code linting
- **TypeScript** for type safety
- **Prettier** for code formatting (integrated with ESLint)

### Adding New Commands

1. Create a new file in `src/commands/`
2. Export a command handler function
3. Register the command in `src/bot.ts`
4. Update the help command with the new command info

Example:
```typescript
// src/commands/example.ts
import { BotContext } from '@/types';
import { logger } from '@/utils/logger';

export const exampleCommand = async (ctx: BotContext): Promise<void> => {
  await ctx.reply('This is an example command!');
  logger.info(`Example command executed for user: ${ctx.from?.username}`);
};
```

## 🚀 Deployment

### GitHub Actions

The project includes automated CI/CD with GitHub Actions:

- **Build & Test**: Runs on every push and PR
- **Docker Build**: Builds and pushes Docker images
- **Security Scanning**: Vulnerability assessment with Trivy
- **Deployment**: Automated deployment to production

### Environment Setup

For production deployment, set these secrets in your GitHub repository:

- `BOT_TOKEN`: Your Telegram bot token
- Other environment variables as needed

## 📊 Monitoring

### Health Checks

The bot includes built-in health monitoring:

- **Docker Health Check**: Automatic container health monitoring
- **Ping Command**: Manual health verification via `/ping`
- **Logging**: Comprehensive request and error logging

### Log Management

Logs are written to:
- **File**: `logs/bot.log` (rotated automatically)
- **Console**: In development mode
- **Structured**: JSON format for production parsing

## 🛡️ Security

### Best Practices Implemented

- **Environment Variables**: Sensitive data stored securely
- **Non-root User**: Docker containers run as non-privileged user
- **Input Validation**: All user inputs validated and sanitized
- **Error Handling**: Graceful error handling without information leakage
- **Security Scanning**: Automated vulnerability scanning in CI/CD

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

- **Issues**: [GitHub Issues](https://github.com/thertxnetworktwo/toolkit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/thertxnetworktwo/toolkit/discussions)

## 🌟 Acknowledgments

- [Telegraf.js](https://telegraf.js.org/) - Modern Telegram Bot Framework
- [Winston](https://github.com/winstonjs/winston) - Logging library
- [TypeScript](https://www.typescriptlang.org/) - Type-safe JavaScript

---

**RTX Network - Building the Future of Decentralized Technology** 🚀