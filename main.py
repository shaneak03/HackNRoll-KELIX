import os
from dotenv import load_dotenv
import telebot
import random
from telebot import types
from controversy_handlers import start_controversy
from objects import Users, Groups, questions
from src.utils.supabase_client import supabase
from never_have_i_ever import never_have_i_ever, handle_poll_answer
from guess_who import guess_who_init, guess_who_details, guess_who_start, guess_who_next, guess_who_end
 
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
        bot.reply_to(message, "👋 Welcome to the IcePick bot! \n\n Here are the commands you can use: \n\n /createprofile - Create a profile \n\n /editprofile - Edit your profile \n")
    else:
        bot.reply_to(message, "👋 Welcome to the IcePick bot! \n\n Here are the commands you can use: \n\n /startgame - Start playing a game \n\n /initgroup - Initialise a group in the chat \n\n Please use /createprofile in a private chat to create your profile.")

# initialise group
@bot.message_handler(commands=['initgroup'])
def init_group(message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        markup = types.InlineKeyboardMarkup()
        join_button = types.InlineKeyboardButton("Join", callback_data="join_group")
        markup.add(join_button)
        
        # Create and store group
        group = Groups(message.chat.id)
        group.update_group_in_DB()
        bot.reply_to(message, "👥 This group has been initialised for IcePick!", reply_markup=markup)
    else:
        bot.reply_to(message, "👾 Please use this command in a group or supergroup. 👾")

@bot.callback_query_handler(func=lambda call: call.data == "join_group")
def handle_join_group(call):
    user_id = call.from_user.id
    print(f"User joingroup call back received: {user_id}")

    # Add logic to handle the user joining the group
    group = Groups(call.chat_instance)
    if group.add_member(user_id) == 1:
        bot.send_message(call.message.chat.id, f"User with ID {user_id} not found! ❌\nCreate your account by messaging @IceAxe_bot")
    else:
        bot.answer_callback_query(call.id, f"User {user_id} has joined the group! 🎉")

# create a profile
@bot.message_handler(commands=['createprofile'])
def create_profile(message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        user_response = supabase.table('User').select('id').eq('id', user_id).execute()
        if user_response.data:
            bot.reply_to(message, "You already have a profile. Would you like to edit it? ✏️\n Use /editprofile to edit")
        else:
            msg = bot.reply_to(message, "What is your name? 🤔")
            bot.register_next_step_handler(msg, ask_q1, {})
    else:
        bot.reply_to(message, "👾 Please use this command in a private chat. 👾")


def ask_q1(message, user_data):
    user_data['name'] = message.text
    qns = random.sample(questions, 5)
    user_data['qns'] = qns
    bot.send_message(message.chat.id, f"Hi {user_data['name']}, let's get to know you better! 📝 Answer the following questions:")
    msg = bot.send_message(message.chat.id, user_data['qns'][0])
    user_data['q1'] = user_data['qns'][0]
    bot.register_next_step_handler(msg, ask_q2, user_data)

def ask_q2(message, user_data):
    user_data['q1_ans'] = message.text
    curr_qn = user_data['qns'][1]
    user_data['q2'] = curr_qn
    msg = bot.send_message(message.chat.id, curr_qn)
    bot.register_next_step_handler(msg, ask_q3, user_data)

def ask_q3(message, user_data):
    user_data['q2_ans'] = message.text
    curr_qn = user_data['qns'][2]
    user_data['q3'] = curr_qn
    msg = bot.send_message(message.chat.id, curr_qn)
    bot.register_next_step_handler(msg, ask_q4, user_data)

def ask_q4(message, user_data):
    user_data['q3_ans'] = message.text
    curr_qn = user_data['qns'][3]
    user_data['q4'] = curr_qn
    msg = bot.send_message(message.chat.id, curr_qn)
    bot.register_next_step_handler(msg, ask_q5, user_data)

def ask_q5(message, user_data):
    user_data['q4_ans'] = message.text
    curr_qn = user_data['qns'][4]
    user_data['q5'] = curr_qn
    msg = bot.send_message(message.chat.id, curr_qn)
    bot.register_next_step_handler(msg, save_profile, user_data)

def save_profile(message, user_data):
    user_data['q5_ans'] = message.text
    user = Users(message.from_user.id, user_data['name'], user_data['q1'], user_data['q2'], user_data['q3'], user_data['q4'], user_data['q5'], user_data['q1_ans'], user_data['q2_ans'], user_data['q3_ans'], user_data['q4_ans'], user_data['q5_ans'])
    user.create_user_in_db()
    msg = bot.send_message(message.chat.id, "Profile Created 🎉")   

# edit profile - edit the user's profile
@bot.message_handler(commands=['editprofile'])
def edit_profile(message):
    if message.chat.type == 'private':
        markup = types.InlineKeyboardMarkup()
        edit_name_button = types.InlineKeyboardButton("Edit Name", callback_data="edit_name")
        markup.add(edit_name_button)
        bot.reply_to(message, "What would you like to edit? ✏️", reply_markup=markup)
    else:
        bot.reply_to(message, "👾 Please use this command in a private chat. 👾")

@bot.callback_query_handler(func=lambda call: call.data == "edit_name")
def handle_edit_name(call):
    msg = bot.send_message(call.message.chat.id, "What is your new name? 🤔")
    bot.register_next_step_handler(msg, save_new_name)

def save_new_name(message):
    new_name = message.text
    bot.reply_to(message, f"Your name has been updated to {new_name}. 🎉")


# start a game
@bot.message_handler(commands=['startgame'])
def prompt_game(message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        markup = types.InlineKeyboardMarkup(row_width=1)
        guess = types.InlineKeyboardButton("Guess Who?", callback_data='guessWho')
        never_have_i_ever_button = types.InlineKeyboardButton("Never Have I Ever", callback_data='neverHaveIEver')
        controversy_button = types.InlineKeyboardButton("Start Controversy", callback_data='startControversy')
        markup.add(guess, never_have_i_ever_button, controversy_button)
        bot.send_message(message.chat.id, "Pick a game! 🎮", reply_markup=markup)
    else:
        bot.reply_to(message, "👾 Please use this command in a group chat. 👾")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    match call.data:
        case "newGame":
            prompt_game(call.message)
        case "guessWho":
            guess_who_init(call.message)
        case "guessWhoDetails":
            guess_who_details(call.message)
        case "guessWhoStart":
            guess_who_start(call)
        case "guessWhoNext":
            guess_who_next(call.message)
        case "guessWhoWin":
            guess_who_end(call.message, True)
        case "guessWhoLose":
            guess_who_end(call.message, False)
        case "neverHaveIEver":
            never_have_i_ever(bot, call.message)
        case "startControversy":
            start_controversy(bot, call.message)
        case _:
            print("missed callback query")

@bot.poll_answer_handler()
def poll_answer_handler(poll_answer):
    handle_poll_answer(bot, poll_answer)

bot.polling()
print("🤖 Bot is polling...")


