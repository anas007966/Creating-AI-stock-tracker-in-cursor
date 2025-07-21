# AI Stock Tracker Telegram Bot

A Python Telegram bot that tracks your selected stocks, sends you price updates every 30 minutes, and allows you to manage your watchlist directly from Telegram.

## Features
- Track real-time prices for your selected stocks
- Receive Telegram notifications every 30 minutes with price changes
- Instantly get updates with the `/update` command
- Manage your watchlist with `/addstock`, `/removestock`, and `/listwatchlist` commands

## Setup

### 1. Clone the Repository
```
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Create a Telegram Bot
- Talk to [@BotFather](https://t.me/BotFather) on Telegram
- Use `/newbot` to create a bot and get your **bot token**

### 4. Get Your Chat ID
- Start a chat with your bot and send any message
- Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` in your browser
- Find your chat ID in the response (e.g., `"chat":{"id":123456789,...}`)

### 5. Configure the Bot
- Open `main.py`
- Replace the placeholders for `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` with your values:
  ```python
  TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
  TELEGRAM_CHAT_ID = YOUR_CHAT_ID
  ```

### 6. Prepare Your Watchlist
- Edit `watchlist.json` to include your desired stock symbols, e.g.:
  ```json
  ["AAPL", "GOOGL", "TSLA"]
  ```

## Usage

### Start the Bot
```
python3 main.py
```

### Telegram Commands
- `/start` — Welcome message
- `/update` — Get an instant stock price update
- `/addstock <SYMBOL>` — Add a stock to your watchlist (e.g., `/addstock AAPL`)
- `/removestock <SYMBOL>` — Remove a stock from your watchlist (e.g., `/removestock TSLA`)
- `/listwatchlist` — List all stocks in your watchlist

### Automatic Updates
- The bot will send you a message every 30 minutes with the latest price changes for your watchlist.

## Notes
- The bot uses [yfinance](https://github.com/ranaroussi/yfinance) for free stock data.
- All data is stored locally in `watchlist.json` and `last_prices.json`.
- Only one instance of the bot should run at a time (otherwise you may see a polling conflict error).

## License
MIT
