import os
from dotenv import load_dotenv
load_dotenv()
import telebot
from SeaPatriot import SeaPatriot
sp = SeaPatriot('dev/code/CONFIG/config.yml')
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler()

def send_welcome(message):
    if message.text.lower() == "ship":
        sp.main()
        bot.send_photo(message.chat.id, open('enhanced_map_with_direction.png', 'rb'))
    elif message.text.lower() == "/start":
        bot.reply_to(message, "Welcome to SeaPatriot Bot! Type 'ship' to get the latest information on a vessel.")
    else:
        response = sp.chat(message.text)
        bot.reply_to(message, response)

bot.infinity_polling()
