import os
from dotenv import load_dotenv
import telebot

# Setting up .env and API_KEY
load_dotenv()

API_KEY = os.getenv('API_KEY')
print(API_KEY)

# Setting up the bot
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the bot!")

bot.polling()