import os
from dotenv import load_dotenv
import telebot
from telebot import types

questions = ["What is your favourite food?",
             "What is your favourite movie?",
             "What is your favourite song?"]

load_dotenv()

TELE_API_KEY = os.getenv('TELE_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Setting up the bot
bot = telebot.TeleBot(TELE_API_KEY)

# start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the bot! \nUse /help to get started")


# help, teach people how to use the bot
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the bot!")


# create a profile
@bot.message_handler(commands=['create-profile'])
def create_profile(message):
    if message.chat.type == 'private':
        msg = bot.reply_to(message, "What is your name?")
        bot.register_next_step_handler(msg, handle_name)
    else:
        bot.reply_to(message, "Please use this command in a private chat.")

def handle_name(message):
    name = message.text
    msg = bot.reply_to(message, f"Nice to meet you, {name}! Write a fun fact about yourself! Please write something that you do not mind revealing to the world. Also your fun fact should not reveal anything about your identity.")
    bot.register_next_step_handler(msg, handle_funFact)

def handle_funFact(message):
    funFact = message.text
    bot.reply_to(message, f"Got it! Your fun fact is: {funFact}.")
    ask_next_question(message, 0, {})

def ask_next_question(message, question_index, answers):
    if question_index < len(questions):
        msg = bot.reply_to(message, questions[question_index])
        bot.register_next_step_handler(msg, lambda m: handle_answer(m, question_index, answers))
    else:
        bot.reply_to(message, f"Thank you for answering all the questions! Here are your answers: {answers}")

def handle_answer(message, question_index, answers):
    answers[questions[question_index]] = message.text
    # Add logic to store the answer in the database

    ask_next_question(message, question_index + 1, answers)

# start-controversy start a controversial topic
@bot.message_handler(commands=['start-controversy'])
def prompt_question(message):
    msg = bot.reply_to(message, "Reply this message with a controversial question to start a poll")
    bot.register_next_step_handler(msg, handle_question)

def handle_question(message):
    question = message.text
    bot.reply_to(message, f"Your question '{question}' has been received and a poll will be created.")
    create_poll(message.chat.id, question)

def create_poll(chat_id, question):
    options = ["A", "B"]
    poll = types.Poll(question=question, options=options, is_anonymous=True)
    bot.send_poll(chat_id, poll.question, poll.options, is_anonymous=poll.is_anonymous)

bot.polling()


