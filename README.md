# Idealista Notifier Bot

## Overview

This project is a Telegram bot that automatically scrapes Idealista for new apartment listings in Barcelona. It filters listings based on predefined criteria and sends real-time notifications via Telegram, including:

- 📍 Location
- 💰 Price
- 🛏️ Rooms
- 📏 Size (m²)
- 🏢 Floor
- 📝 Description
- 🔗 Direct link to the listing

## Project Structure

```text
idealista-notifier/
│── src/
│   ├── scraper.py          # Scrapes Idealista & sends Telegram notifications
│── .env                    # Stores API keys (excluded from Git)
│── requirements.txt        # Python dependencies
│── Dockerfile              # Container configuration
│── docker-compose.yml      # Deployment configuration
│── README.md               # Project documentation
```

## How It Works

1. The script scrapes Idealista every 2 minutes
2. It filters out unwanted areas (e.g., Raval, Gòtic)
3. If a new listing appears, it extracts:
    - Location, price, size, rooms, floor, and description
4. It sends a formatted message to your Telegram bot

## Setup & Installation

1. Clone the Repository

```bash
git clone https://github.com/martin0995/idealista-notifier.git
cd idealista-notifier
```

2. Install Dependencies

```bash
pip install -r requirements.txt
```

3. Set Up Environment Variables
Create a `.env` file in the root directory and add:

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

- **TELEGRAM_BOT_TOKEN** → Get this from Telegram's @BotFather
- **TELEGRAM_CHAT_ID** → Get this using the `/getUpdates` API

4. Run the Bot

```bash
python3 src/scraper.py
```

## Docker Setup

### Run Locally with Docker

To run the bot using Docker:

```bash
docker build -t idealista-bot .
docker run -d --restart unless-stopped --name idealista-bot idealista-bot
```

### Run with Docker Compose

```bash
docker-compose up -d
```

This ensures the bot persists data and auto-restarts if it stops.

## Deploy to Railway.app

1. Install Railway CLI

```bash
curl -fsSL https://railway.app/install.sh | sh
railway login
```

2. Link Project & Deploy

```bash
railway init
railway up
```

3. Set Environment Variables

```bash
railway variables --set "TELEGRAM_BOT_TOKEN=your_bot_token_here" --set "TELEGRAM_CHAT_ID=your_chat_id_here"
```

4. Check Logs & Status

```bash
railway logs -f
railway status
```

The bot will now run 24/7, even if you turn off your computer.

## Telegram Bot Link

Try it out: https://t.me/Idealista_Notifier_Bot

## Contributing

Feel free to open issues or submit a pull request to improve the project!