import os
from dotenv import load_dotenv
import telebot

load_dotenv()

TELE_API_KEY = os.getenv('TELE_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

print(TELE_API_KEY)

# Setting up the bot
bot = telebot.TeleBot(TELE_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the bot!")

bot.polling()