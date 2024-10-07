import logging
from telebot import TeleBot
from SeaPatriot import SeaPatriot
import os

# Set up the logger
logging.basicConfig(
    filename='bot_logs.log',  # Log file where logs will be stored
    level=logging.INFO,  # Log level, INFO captures general events
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
)

# Create SeaPatriot instance
sp = SeaPatriot('dev/code/CONFIG/config.yml')

# Create the bot instance
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = TeleBot(BOT_TOKEN)

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Welcome to SeaPatriot Bot! Type 'ship' to get the latest information on a vessel.")
    
    # Log the interaction
    logging.info(f"New user started conversation, chat_id: {chat_id}")

# Message handler for all messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id  # Get the chat ID of the user
    user_input = message.text  # Get the user input (message text)

    # Log the user input and chat_id
    logging.info(f"Received input from chat_id: {chat_id}, input: {user_input}")
    
    if user_input.lower() == "ship" or user_input.lower() == "/ship":
        # Perform ship tracking operation and send map
        sp.main()
        bot.send_photo(chat_id, open('enhanced_map_with_direction.png', 'rb'))
    else:
        # Process the user's message with the SeaPatriot chat function
        response = sp.chat(user_input, chat_id=chat_id)
        
        # Log the bot's response
        logging.info(f"Sent response to chat_id: {chat_id}, response: {response}")
        
        # Reply with the bot's response
        bot.reply_to(message, response)

# Start the bot
bot.infinity_polling()
