import os
from dotenv import load_dotenv
import telebot
from telebot import types
import random
import csv
from src.utils.supabase_client import supabase

load_dotenv()

TELE_API_KEY = os.getenv('TELE_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

bot = telebot.TeleBot(TELE_API_KEY)

def pull_data(call):
    with open("guessWhoData.txt", "w", newline='') as csvfile:
        file = csv.writer(csvfile)
        print(call.chat_instance)
        query = supabase.table("Groups").select("members_id").eq("grp_id", call.chat_instance).execute()
        author = random.choice(query.data[0]["members_id"])

        s = supabase.table('User').select('*').eq('id', author).execute()
        print(s)

        qs_key =["q1", "q2", "q3", "q4", "q5"]
        for key in qs_key:
            file.writerow([s.data[0][key], s.data[0][key + "_ans"]])
    print("Data pulled")

def guess_who_init(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    rules = types.InlineKeyboardButton("Details", callback_data='guessWhoDetails')
    start = types.InlineKeyboardButton("Start game!", callback_data='guessWhoStart')
    markup.add(rules, start)
    
    welcome_msg = "Welcome to Guess Who? Attempt to guess who wrote the answers with as little hints as possible. The twist? The authors will have to mislead the group to hide their identity!"

    bot.send_message(message.chat.id, text = welcome_msg, reply_markup=markup)
    print("guess_who_init() finish execution")

def guess_who_details(message):
    markup = types.InlineKeyboardMarkup(row_width = 1)
    back = types.InlineKeyboardButton("Return", callback_data="guessWho")
    markup.add(back)
    
    details = "In this game, the bot will randomly select a user as the mysterious author.\n\nThe bot will then present a question along with one answer written by that person. The group's task is to guess who the author is, but beware—the author will actively try to mislead the group to protect their identity!\n\nThe group gets one guess per round. If the guess is incorrect, the bot will reveal another answer written by the same author to give the group more clues. The game continues until the group correctly identifies the author or uses up a total of five guesses.\n\nCan you uncover the truth, or will the author successfully hide in plain sight? Good luck!"
    bot.send_message(message.chat.id, text = details, reply_markup=markup)

def guess_who_start(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    ghnext = types.InlineKeyboardButton("Next clue..", callback_data='guessWhoNext')
    ghend = types.InlineKeyboardButton("Mysterious Author Found!", callback_data='guessWhoWin')
    markup.add(ghnext, ghend)
    
    pull_data(call)

    with open("guessWhoData.txt", "r") as csvfile:
        data = csv.reader(csvfile)
        data = list(data)
    first = random.choice(data)
    print(data)
    bot.send_message(call.message.chat.id, text = f"First clue!~\n\nThe question is : {first[0]}\n\nThe answer is : {first[1]}", reply_markup=markup)

    data.remove(first)  # Remove the selected row
    data = [row for row in data if row]  # Filter out empty rows
    with open("guessWhoData.txt", "w", newline='') as csvfile:
        file = csv.writer(csvfile)
        for row in data:
            file.writerow(row)
    
    
    #Deal with 5 guess endgame
def guess_who_next(message):
    with open("guessWhoData.txt", "r") as csvfile:
        data = csv.reader(csvfile)
        data = list(data)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    if len(data) > 1:
        ghnext = types.InlineKeyboardButton("Next clue..", callback_data='guessWhoNext')
        ghend = types.InlineKeyboardButton("Mysterious Author Found!", callback_data='guessWhoWin')
        markup.add(ghnext, ghend)
    else:
        ghnext = types.InlineKeyboardButton("Last guess.....", callback_data='guessWhoLose')
        ghend = types.InlineKeyboardButton("Mysterious Author Found!", callback_data='guessWhoWin')
        markup.add(ghnext, ghend)
    demeanings = [
  "Is that the best you can do?",
  "Seriously? You can do better than that!",
  "That was weak, come on!",
  "Not even close, try again!",
  "I expected more from you!",
  "That was an easy one, what happened?",
  "You're better than that!",
  "Really? That's your final answer?",
  "I thought you'd be quicker than that!",
  "That guess was a stretch!"
]
    demeaning = random.choice(list(demeanings))
    next_data = random.choice(data)
    print("data :", data)
    print(next_data)
    bot.send_message(message.chat.id, text = demeaning + f"\n\nThe question is : {next_data[0]}\n\nThe answer is : {next_data[1]}", reply_markup=markup)
    
    data.remove(next_data)  # Remove the selected row
    data = [row for row in data if row]  # Filter out empty rows
    with open("guessWhoData.txt", "w", newline='') as csvfile:
        file = csv.writer(csvfile)
        for row in data:
            file.writerow(row)

def guess_who_end(message, win):
    markup = types.InlineKeyboardMarkup(row_width=1)
    one = types.InlineKeyboardButton("Play again?", callback_data='guessWho')
    two = types.InlineKeyboardButton("Play Another Game", callback_data = "newGame")
    markup.add(one, two)
    if win:
        win_msg = "Congratulations! You have successfully identified the mysterious author!"
    else:
        win_msg = "You have failed to identify the mysterious author. Better luck next time!"
        
    bot.send_message(message.chat.id, win_msg + "\n\nGame ended. Thank you for playing!", reply_markup=markup)
    print("ended game")