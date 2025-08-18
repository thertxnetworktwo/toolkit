# RTX Network Toolkit Telegram Bot

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org/)

A comprehensive, professional Telegram bot for RTX Network with modern TypeScript implementation, robust error handling, and production-ready deployment.

## 🚀 Features

### Core Bot Commands
- **`/start`** - Welcome message with RTX Network branding
- **`/help`** - Display available commands and usage instructions
- **`/about`** - Information about RTX Network and the toolkit
- **`/ping`** - Health check with response time and uptime

### Technical Features
- ✅ **TypeScript** implementation with strict typing
- ✅ **Telegraf** framework for robust bot functionality
- ✅ **Winston** logging with structured output
- ✅ **Professional error handling** and recovery
- ✅ **Docker containerization** with multi-stage builds
- ✅ **Environment-based configuration**
- ✅ **Health checks** and monitoring
- ✅ **Graceful shutdown** handling
- ✅ **Production-ready** deployment setup

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm 8+
- Docker (optional, for containerized deployment)
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/thertxnetworktwo/toolkit.git
   cd toolkit
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your bot token and configuration
   ```

4. **Build the project**
   ```bash
   npm run build
   ```

5. **Start development server**
   ```bash
   npm run dev
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Required
BOT_TOKEN=your_telegram_bot_token_here

# Optional
BOT_NAME=RTX Toolkit Bot
BOT_USERNAME=rtx_toolkit_bot
LOG_LEVEL=info
LOG_FORMAT=json
NODE_ENV=development
PORT=3000

# Production Webhook (optional)
WEBHOOK_URL=https://your-domain.com
WEBHOOK_PORT=8443
WEBHOOK_SECRET_TOKEN=your_secret_token
```

### Getting a Bot Token

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Copy the token to your `.env` file

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Build and start**
   ```bash
   docker-compose up -d
   ```

3. **View logs**
   ```bash
   docker-compose logs -f rtx-toolkit-bot
   ```

4. **Stop the bot**
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image**
   ```bash
   docker build -t rtx-toolkit-bot .
   ```

2. **Run the container**
   ```bash
   docker run -d \
     --name rtx-toolkit-bot \
     --env-file .env \
     -p 8443:8443 \
     --restart unless-stopped \
     rtx-toolkit-bot
   ```

## 🛠️ Development

### Available Scripts

```bash
# Development
npm run dev          # Start with hot reload
npm run build        # Build for production
npm run start        # Start production build

# Code Quality
npm run lint         # Run ESLint
npm run lint:fix     # Fix ESLint issues
npm run format       # Format with Prettier

# Docker
npm run build:docker # Build Docker image
```

### Project Structure

```
├── src/
│   ├── bot.ts              # Main bot application
│   ├── commands/
│   │   └── index.ts        # Command handlers
│   └── utils/
│       └── helpers.ts      # Utility functions
├── dist/                   # Built JavaScript files
├── package.json           # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── .eslintrc.json         # ESLint configuration
├── .prettierrc            # Prettier configuration
├── Dockerfile             # Docker build instructions
├── docker-compose.yml     # Docker Compose setup
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

### Code Style

This project uses:
- **ESLint** for code linting
- **Prettier** for code formatting
- **TypeScript strict mode** for type safety

Run `npm run lint:fix` and `npm run format` before committing.

## 📊 Monitoring & Logging

### Logging
The bot uses Winston for structured logging with the following levels:
- `error` - Error conditions
- `warn` - Warning conditions  
- `info` - Informational messages
- `debug` - Debug-level messages

### Health Checks
- Docker health check endpoint
- `/ping` command for manual health verification
- Uptime and response time monitoring

### Production Monitoring
For production deployments, consider:
- Log aggregation (ELK stack, Grafana Loki)
- Metrics collection (Prometheus)
- Alerting (Grafana, PagerDuty)

## 🔧 Bot Commands

### `/start`
Welcome message introducing the bot and RTX Network.

### `/help` 
Comprehensive list of available commands with usage instructions.

### `/about`
Information about RTX Network, the toolkit, and contact links.

### `/ping`
Health check showing:
- Bot status
- Response time
- Uptime
- System information

## 🛡️ Security Considerations

- Environment variables for sensitive configuration
- Input sanitization and validation
- Error handling without information disclosure
- Docker security best practices
- Non-root user in container

## 🚀 Production Deployment

### Webhook Mode (Recommended)
For production, use webhook mode instead of long polling:

1. Set up HTTPS endpoint
2. Configure webhook environment variables
3. Deploy with proper SSL certificates

### Scaling Considerations
- Use webhook mode for better performance
- Implement rate limiting
- Consider load balancing for high traffic
- Monitor resource usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Open a GitHub issue for bugs or feature requests
- **Community**: Join the RTX Network community channels

## 🔗 Links

- **RTX Network**: [rtxnetwork.io](https://rtxnetwork.io)
- **Documentation**: [docs.rtxnetwork.io](https://docs.rtxnetwork.io)  
- **GitHub**: [github.com/thertxnetworktwo](https://github.com/thertxnetworktwo)
- **Telegram Bot API**: [core.telegram.org/bots/api](https://core.telegram.org/bots/api)
- **Telegraf Framework**: [telegraf.js.org](https://telegraf.js.org)

---

Built with ❤️ by the RTX Network team.