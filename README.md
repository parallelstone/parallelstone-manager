# Parallelstone Manager

FastAPI 기반 마인크래프트 서버 관리 API로, RabbitMQ를 통한 멀티채널 알림 시스템을 제공합니다.

## Features

- 🎮 **Minecraft Server Control**: RCON 프로토콜을 통한 서버 제어 및 명령 실행
- 📢 **Multi-Channel Notifications**: RabbitMQ 기반 멀티채널 알림 시스템
  - Telegram
  - Discord  
  - Slack
- 🚀 **Async Architecture**: 비동기 I/O를 활용한 고성능 처리
- 🔄 **Persistent Connections**: RCON 연결 재사용으로 효율성 향상
- ✅ **Type Safety**: Pydantic을 통한 데이터 검증

## Tech Stack

- **Language**: Python 3.12+
- **Web Framework**: FastAPI 0.115.14
- **ASGI Server**: Uvicorn 0.35.0
- **Message Queue**: RabbitMQ (aio-pika)
- **Testing**: pytest with async support

## Architecture

```
┌─────────────────┐
│   FastAPI App   │
│   (main.py)     │
└────────┬────────┘
         │
    ┌────┴─────┬──────────┬──────────┐
    │          │          │          │
┌───▼───┐  ┌──▼────┐  ┌──▼────┐  ┌───▼─────┐
│Server │  │Players│  │RCON   │  │RabbitMQ │
│Router │  │Router │  │Service│  │Publisher│
└───┬───┘  └───────┘  └───────┘  └───┬─────┘
    │                                │
    └────────────────────────────────┘
                                     │
                 ┌───────────────────┴────────────────┐
                 │   RabbitMQ Exchange (topic)        │
                 │   "notification_router"            │
                 └┬────────────┬────────────┬─────────┘
                  │            │            │
          ┌───────▼──┐  ┌──────▼───┐   ┌────▼──────┐
          │Telegram  │  │Discord   │   │Slack      │
          │Consumer  │  │Consumer  │   │Consumer   │
          └──────────┘  └──────────┘   └───────────┘
```

## Installation

### Prerequisites

- Python 3.12+
- RabbitMQ server
- Minecraft server with RCON enabled
- uv (recommended) or pip

### Setup

1. Clone the repository
```bash
git clone https://github.com/parallelstone/parallelstone-manager
cd parallelstone-manager
```

2. Install dependencies
```bash
# Using uv (recommended)
uv pip install -e ".[dev]"

# Or using pip
pip install -e ".[dev]"
```

3. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your settings
```

Required environment variables:
```bash
# Minecraft Server
MINECRAFT_HOST=localhost
MINECRAFT_PORT=25575
MINECRAFT_PASSWORD=your_rcon_password

# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VIRTUAL_HOST=/parallel

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id

# Discord (optional)
DISCORD_BOT_TOKEN=your_token
DISCORD_CHANNEL_ID=your_channel_id

# Slack (optional)
SLACK_BOT_TOKEN=your_token
SLACK_CHANNEL_ID=your_channel_id
```

## Usage

### Start the API Server

The FastAPI server automatically starts all consumer processes:

```bash
uvicorn parallelstone_manager.main:app
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

### API Endpoints

All endpoints return a unified response format:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "key": "value"
  }
}
```

#### Server Control
- `POST /server/start` - Start the server (placeholder)
- `POST /server/stop` - Stop the server (placeholder)
- `POST /server/restart` - Restart the server (placeholder)
- `GET /server/status` - Get server status
- `GET /server/test-connection` - Test RCON connection
- `GET /server/commands?cmd=<command>` - Execute RCON command
- `POST /server/announce?msg=<message>` - Broadcast message to all players
- `POST /server/gamerule?rule=<rule>&value=<value>` - Change game rule

**Example Response:**
```json
{
  "success": true,
  "message": "Command executed successfully",
  "data": {
    "result": "There are 3 of a max of 20 players online"
  }
}
```

#### Player Management
- `GET /players/` - Get player count
- `GET /players/player_list` - Get list of online players
- `POST /players/kick?player_name=<name>` - Kick a player
- `POST /players/ban?player_name=<name>` - Ban a player
- `POST /players/pardon?player_name=<name>` - Pardon a banned player

**Example Response:**
```json
{
  "success": true,
  "message": "Player kicked successfully",
  "data": {
    "result": "Kicked player123"
  }
}
```

### Run Individual Consumers (for debugging)

```bash
python -m parallelstone_manager.consumers.telegram_sender
python -m parallelstone_manager.consumers.discord_sender
python -m parallelstone_manager.consumers.slack_sender
```

## Development

### Project Structure

```
parallelstone-manager/
├── parallelstone_manager/
│   ├── main.py                 # FastAPI app entry point
│   ├── routers/                # API endpoints
│   │   ├── server.py
│   │   └── players.py
│   ├── services/               # Business logic
│   │   ├── rcon.py            # RCON client
│   │   └── rabbitmq.py        # RabbitMQ integration
│   ├── consumers/              # Message consumers
│   │   ├── consumer.py        # Base consumer
│   │   ├── telegram_sender.py
│   │   ├── discord_sender.py
│   │   └── slack_sender.py
│   ├── models/                 # Pydantic models
│   └── core/                   # Configuration
│       ├── config.py
│       └── dependencies.py
└── tests/
    ├── unit/
    └── integration/
```

## RabbitMQ Message Flow

Messages are routed through a topic exchange:

```
Exchange: "notification_router" (type: topic)
├── telegram_queue → binding: "#.telegram.#"
├── discord_queue  → binding: "#.discord.#"
└── slack_queue    → binding: "#.slack.#"
```

Publish messages with routing keys like:
- `notification.telegram.alert`
- `notification.discord.info`
- `notification.slack.warning`

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.