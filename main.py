import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import yfinance as yf
import json
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Inserted Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = 

WATCHLIST_FILE = 'watchlist.json'
LAST_PRICES_FILE = 'last_prices.json'

# Load watchlist from file
def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r') as f:
            return json.load(f)
    return []

# Load last known prices from file
def load_last_prices():
    if os.path.exists(LAST_PRICES_FILE):
        with open(LAST_PRICES_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save last known prices to file
def save_last_prices(prices):
    with open(LAST_PRICES_FILE, 'w') as f:
        json.dump(prices, f)

def save_watchlist(watchlist):
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(watchlist, f)

# Fetch current prices for the watchlist
def fetch_current_prices(symbols):
    prices = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.info.get('regularMarketPrice')
            if price is not None:
                prices[symbol] = price
        except Exception as e:
            logging.warning(f"Failed to fetch price for {symbol}: {e}")
    return prices

# Format the price change message
def format_price_message(current, previous):
    lines = []
    for symbol, price in current.items():
        prev_price = previous.get(symbol)
        if prev_price is not None:
            change = price - prev_price
            percent = (change / prev_price) * 100 if prev_price != 0 else 0
            direction = '⬆️' if change > 0 else ('⬇️' if change < 0 else '➡️')
            lines.append(f"{symbol}: {price:.2f} ({direction} {change:+.2f}, {percent:+.2f}%)")
        else:
            lines.append(f"{symbol}: {price:.2f} (new)")
    return '\n'.join(lines)

# Periodic stock check and notification
def check_stocks_and_notify(app):
    watchlist = load_watchlist()
    if not watchlist:
        logging.info("Watchlist is empty.")
        return
    last_prices = load_last_prices()
    current_prices = fetch_current_prices(watchlist)
    if not current_prices:
        logging.info("No prices fetched.")
        return
    message = format_price_message(current_prices, last_prices)
    # Send message via Telegram
    async def send_message():
        await app.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"Stock Price Update:\n{message}")
    import asyncio
    asyncio.run(send_message())
    # Save current prices for next comparison
    save_last_prices(current_prices)

# New: Command handler for /update
async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    watchlist = load_watchlist()
    if not watchlist:
        await update.message.reply_text("Watchlist is empty.")
        return
    last_prices = load_last_prices()
    current_prices = fetch_current_prices(watchlist)
    if not current_prices:
        await update.message.reply_text("No prices fetched.")
        return
    message = format_price_message(current_prices, last_prices)
    await update.message.reply_text(f"Stock Price Update:\n{message}")
    save_last_prices(current_prices)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to the AI Stock Tracker Bot!')

# Add stock to watchlist
async def addstock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /addstock <SYMBOL>")
        return
    symbol = context.args[0].upper()
    watchlist = load_watchlist()
    if symbol in watchlist:
        await update.message.reply_text(f"{symbol} is already in your watchlist.")
        return
    watchlist.append(symbol)
    save_watchlist(watchlist)
    await update.message.reply_text(f"Added {symbol} to your watchlist.")

# Remove stock from watchlist
async def removestock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /removestock <SYMBOL>")
        return
    symbol = context.args[0].upper()
    watchlist = load_watchlist()
    if symbol not in watchlist:
        await update.message.reply_text(f"{symbol} is not in your watchlist.")
        return
    watchlist.remove(symbol)
    save_watchlist(watchlist)
    await update.message.reply_text(f"Removed {symbol} from your watchlist.")

# List current watchlist
async def listwatchlist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    watchlist = load_watchlist()
    if not watchlist:
        await update.message.reply_text("Your watchlist is empty.")
        return
    await update.message.reply_text("Your watchlist:\n" + "\n".join(watchlist))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('update', update_command))
    app.add_handler(CommandHandler('addstock', addstock_command))
    app.add_handler(CommandHandler('removestock', removestock_command))
    app.add_handler(CommandHandler('listwatchlist', listwatchlist_command))

    # Set up scheduler for periodic stock checks
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_stocks_and_notify, 'interval', minutes=30, args=[app])
    scheduler.start()

    print('Bot is running...')
    app.run_polling() 
