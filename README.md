# RTX Toolkit Bot

A powerful Telegram bot built with Node.js, TypeScript, and modern development practices. RTX Toolkit provides essential tools and utilities for the RTX Network community.

## 🚀 Features

- **Modern Tech Stack**: Built with Node.js, TypeScript, and Telegraf
- **Command-Based Interface**: Simple and intuitive command system
- **Production Ready**: Comprehensive error handling, logging, and monitoring
- **Docker Support**: Full containerization for easy deployment
- **CI/CD Pipeline**: Automated deployment with GitHub Actions
- **Type Safety**: Full TypeScript implementation with strict typing
- **Structured Logging**: Winston-based logging with multiple levels
- **Health Checks**: Built-in health monitoring for reliability

## 📋 Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and quick start guide |
| `/help` | Display available commands and usage |
| `/about` | Information about RTX Toolkit Bot |

## 🛠️ Installation

### Prerequisites

- Node.js 18 or higher
- npm or yarn
- Docker (for containerized deployment)
- Telegram Bot Token (from @BotFather)

### Local Development

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
   # Edit .env and add your BOT_TOKEN
   ```

4. **Build the project**
   ```bash
   npm run build
   ```

5. **Start development server**
   ```bash
   npm run dev
   ```

### Production Deployment

#### Docker Compose (Recommended)

1. **Clone and configure**
   ```bash
   git clone https://github.com/thertxnetworktwo/toolkit.git
   cd toolkit
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Deploy with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Check status**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

#### Manual Docker Deployment

1. **Build the image**
   ```bash
   docker build -t rtx-toolkit-bot .
   ```

2. **Run the container**
   ```bash
   docker run -d \
     --name rtx-toolkit-bot \
     --restart unless-stopped \
     -e BOT_TOKEN=your_bot_token \
     -e NODE_ENV=production \
     -p 3000:3000 \
     -v ./logs:/app/logs \
     rtx-toolkit-bot
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BOT_TOKEN` | Telegram Bot Token from @BotFather | - | ✅ |
| `NODE_ENV` | Environment mode | `development` | ❌ |
| `LOG_LEVEL` | Logging level (error/warn/info/debug) | `info` | ❌ |
| `PORT` | Health check server port | `3000` | ❌ |

### Getting a Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the provided token to your `.env` file

## 🏗️ Project Structure

```
/
├── src/
│   ├── bot.ts              # Main bot application
│   ├── handlers/           # Command handlers
│   │   ├── index.ts        # Handler exports
│   │   ├── start.ts        # /start command
│   │   ├── help.ts         # /help command
│   │   └── about.ts        # /about command
│   ├── config/
│   │   └── index.ts        # Configuration management
│   └── utils/
│       └── logger.ts       # Logging utility
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Docker compose setup
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
├── .env.example            # Environment template
├── .github/workflows/      # CI/CD pipeline
├── .dockerignore           # Docker ignore rules
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🚀 Deployment

### Automated Deployment (GitHub Actions)

This project includes a complete CI/CD pipeline that automatically deploys to your server when code is pushed to the main branch.

#### Setup Requirements

1. **Server Setup**
   - Linux server with Docker and Docker Compose installed
   - SSH access configured

2. **GitHub Secrets Configuration**
   
   Add these secrets to your GitHub repository settings:
   
   | Secret | Description |
   |--------|-------------|
   | `SERVER_HOST` | Your server's IP address or domain |
   | `SERVER_USER` | SSH username |
   | `SERVER_SSH_KEY` | Private SSH key for server access |
   | `SERVER_PORT` | SSH port (optional, defaults to 22) |

3. **Server Preparation**
   ```bash
   # On your server, create deployment directory
   mkdir -p ~/rtx-toolkit-deployment
   cd ~/rtx-toolkit-deployment
   
   # Create .env file with your bot token
   cp .env.example .env
   # Edit .env with your BOT_TOKEN
   ```

4. **Deploy**
   - Push to main branch
   - GitHub Actions will automatically build and deploy
   - Monitor deployment in the Actions tab

### Manual Server Deployment

1. **Prepare server**
   ```bash
   # Install Docker and Docker Compose
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo usermod -aG docker $USER
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **Deploy application**
   ```bash
   git clone https://github.com/thertxnetworktwo/toolkit.git
   cd toolkit
   cp .env.example .env
   # Configure .env file
   docker-compose up -d
   ```

## 📊 Monitoring

### Health Checks

The bot includes built-in health monitoring:

- **HTTP Endpoint**: `http://localhost:3000` (configurable port)
- **Docker Health Check**: Automatic container health monitoring
- **Logging**: Comprehensive logging with Winston

### Logs

Logs are stored in the `logs/` directory:

- `error.log`: Error-level logs only
- `combined.log`: All log levels
- Console output: Development environment only

### Checking Bot Status

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f

# Check health
curl http://localhost:3000
```

## 🔧 Development

### Available Scripts

| Script | Description |
|--------|-------------|
| `npm run build` | Compile TypeScript to JavaScript |
| `npm start` | Start the production bot |
| `npm run dev` | Start development server with ts-node |
| `npm run watch` | Watch for changes and recompile |
| `npm run clean` | Remove build artifacts |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Fix ESLint issues automatically |

### Adding New Commands

1. **Create handler file** in `src/handlers/`:
   ```typescript
   import { Context } from 'telegraf';
   import logger from '../utils/logger';

   export const myCommandHandler = async (ctx: Context): Promise<void> => {
     try {
       await ctx.reply('Hello from my command!');
       logger.info(`My command executed by user: ${ctx.from?.id}`);
     } catch (error) {
       logger.error('Error in my command handler:', error);
       await ctx.reply('Sorry, something went wrong.');
     }
   };
   ```

2. **Export handler** in `src/handlers/index.ts`:
   ```typescript
   export { myCommandHandler } from './mycommand';
   ```

3. **Register command** in `src/bot.ts`:
   ```typescript
   import { myCommandHandler } from './handlers';
   bot.command('mycommand', myCommandHandler);
   ```

### Code Style

- **TypeScript**: Strict mode enabled with comprehensive type checking
- **ESLint**: Configured with TypeScript-specific rules
- **Formatting**: Consistent code style enforced
- **Error Handling**: All async operations wrapped in try-catch blocks
- **Logging**: Structured logging for debugging and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/thertxnetworktwo/toolkit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/thertxnetworktwo/toolkit/discussions)
- **Documentation**: This README and inline code comments

## 🔗 Links

- **Repository**: [https://github.com/thertxnetworktwo/toolkit](https://github.com/thertxnetworktwo/toolkit)
- **Telegraf Documentation**: [https://telegraf.js.org/](https://telegraf.js.org/)
- **Telegram Bot API**: [https://core.telegram.org/bots/api](https://core.telegram.org/bots/api)

---

Made with ❤️ by [RTX Network](https://github.com/thertxnetworktwo)