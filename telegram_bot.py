from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import requests


print('Starting up bot...')

TOKEN: Final = '6284867269:AAEr9iAXfMIyIVd9g8nLXyJDq5EoUeCWHu8'
BOT_USERNAME: Final = '@quick_crypto_bot'

url = "https://binance43.p.rapidapi.com/ticker/price"


headers = {
	"content-type": "application/octet-stream",
	"X-RapidAPI-Key": "2e184b4b50mshff77d69c9848965p1c24c5jsn1fe70c3a78cb",
	"X-RapidAPI-Host": "binance43.p.rapidapi.com"
}

#response = requests.get("https://api.coinranking.com/v2/coins")



# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! I\'m a bot. What\'s up?')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')


# Lets us use the /custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')


def handle_response(text: str) -> str: 
    # Create your own response logic
    processed: str = text
    querystring = {"symbol":text.upper()}
    response = requests.get(url, headers=headers, params=querystring)

    price = json.loads(response.text)["price"]
    symbol = json.loads(response.text)["symbol"]
    return f'The Price of {symbol} is {price}'



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  #We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)




# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
