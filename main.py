import os
from dotenv import load_dotenv
import telebot
from telebot import types
from controversy_handlers import register_controversy_handlers

questions = ["What is your favourite food?",
             "What is your favourite movie?",
             "What is your favourite song?"]

load_dotenv()

TELE_API_KEY = os.getenv('TELE_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Setting up the bot
bot = telebot.TeleBot(TELE_API_KEY)

# help/start, teach people how to use the bot
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    if message.chat.type == 'private':
        bot.reply_to(message, "Welcome to the IcePick bot! \n\n Here are the commands you can use: \n\n /createProfile - Create a profile \n\n /editProfile - Edit your profile \n")
    else:
        bot.reply_to(message, "Welcome to the IcePick bot! \n\n Here are the commands you can use: \n\n /startGame - Start playing a game \n\n /initGroup - Initialise a group in the chat \n\n Please use /createProfile in a private chat to create your profile.")

# initialise group
@bot.message_handler(commands=['initGroup'])
def init_group(message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        markup = types.InlineKeyboardMarkup()
        join_button = types.InlineKeyboardButton("Join", callback_data="join_group")
        markup.add(join_button)
        bot.reply_to(message, "This group has been initialised for IcePick!", reply_markup=markup)
    else:
        bot.reply_to(message, "Please use this command in a group or supergroup.")

@bot.callback_query_handler(func=lambda call: call.data == "join_group")
def handle_join_group(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id, f"User {user_id} has joined the group!")
    # Add logic to handle the user joining the group


# create a profile
@bot.message_handler(commands=['createProfile'])
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


# edit profile - edit the user's profile
@bot.message_handler(commands=['editProfile'])
def edit_profile(message):
    if message.chat.type == 'private':
        markup = types.InlineKeyboardMarkup()
        edit_name_button = types.InlineKeyboardButton("Edit Name", callback_data="edit_name")
        markup.add(edit_name_button)
        bot.reply_to(message, "What would you like to edit?", reply_markup=markup)
    else:
        bot.reply_to(message, "Please use this command in a private chat.")

@bot.callback_query_handler(func=lambda call: call.data == "edit_name")
def handle_edit_name(call):
    msg = bot.send_message(call.message.chat.id, "What is your new name?")
    bot.register_next_step_handler(msg, save_new_name)

def save_new_name(message):
    new_name = message.text
    bot.reply_to(message, f"Your name has been updated to {new_name}.")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"Your user ID is {user_id}")


# start a game
@bot.message_handler(commands=['startGame'])
def prompt_game(message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        markup = types.InlineKeyboardMarkup(row_width=2)
        guess = types.InlineKeyboardButton("Guess Who?", callback_data='guess')
        markup.add(guess)
        bot.send_message(message.chat.id, "Pick a game!", reply_markup=markup)
    else:
        bot.reply_to(message, "Please use this command in a group chat.")
                                                                          
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'guess':
        bot.send_message(call.message.chat.id, "Starting Guess Who?...")
        #guess_who_start()


# start-controversy start a controversial topic
@bot.message_handler(commands=['startControversy'])
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


