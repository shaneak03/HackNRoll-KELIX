import os
import telebot
from telebot import types
import random

TELE_API_KEY = os.getenv('TELE_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

bot = telebot.TeleBot(TELE_API_KEY)

def fetch_qns():
    qns = ["Who is the most likely to be a secret agent?", "Who is the most likely to be a superhero?", "Who is the most likely to be a villain?", "Who is the most likely to be a spy?", "Who is the most likely to be a double agent?"]

def burning_bridges_init(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    rules = types.InlineKeyboardButton("Details", callback_data='burningBridgesDetails')
    start = types.InlineKeyboardButton("Start game!", callback_data='burningBridgesStart')
    markup.add(rules, start)
    
    welcome_msg = "Welcome to Burning Bridges! The first player will answer a mystery question regarding people in the group.\n\nAfterwards, the 2 involved players will play a game.\n\nIf the first person loses, the question will be revealed to the group!"
    bot.send_message(message.chat.id, text = welcome_msg, reply_markup=markup)
    print("burning_bridges_init() finish execution")

def burning_bridges_details(message):
    markup = types.InlineKeyboardMarkup(row_width = 1)
    back = types.InlineKeyboardButton("Return", callback_data="burningBridges")
    markup.add(back)
    
    details = "The first player is given a secret question and must answer by naming someone in the group.\n\nThen, the first player and the chosen person play a two-player game. If the first player loses, the secret question is revealed to the group. If they win, they escape without revealing the question.\n\nThe chosen person then becomes the one to answer a new secret question in the next round."
    bot.send_message(message.chat.id, text = details, reply_markup=markup)

def burning_bridges_start(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    join = types.InlineKeyboardButton("Join game!", callback_data='burningBridgesJoin')
    start = types.InlineKeyboardButton("Start game!!", callback_data='burningBridgesBegin')
    markup.add(join, start)

    with(open("burning_bridges.txt", "w")) as f:
        f.close()

    bot.send_message(call.message.chat.id, text = "The game is about to start! Join now!", reply_markup=markup)

def burning_bridges_join(call):
    print(call.from_user.id, "from user id")
    bot.send_message(call.from_user.id, 'Successfully joined Burning Bridges game!')

    with open("burning_bridges.txt", "r") as f:
        lines = list(f.readlines())

    with open("burning_bridges.txt", "a") as f:
        if True or str(call.from_user.id) not in lines: ##REMOVE TRUE
            f.write(f"{call.from_user.id}\n")
        else:
            bot.send_message(call.from_user.id, 'You have already joined the game!')

def burning_bridges_begin(call):
    print("Game has begun!")
    with open("burning_bridges.txt", "r") as f:
        players = []
        for line in f:
            players.append(line.strip())
    bot.send_message(call.message.chat.id, f"The game has begun! Good luck!\n\nThe players are : {players}")
    first = random.choice(players)
    print(first, "is first")
    burning_bridges_turn(first)

def burning_bridges_turn(player):
    qn = fetch_qns()

    with open("burning_bridges.txt", "r") as f:
        players = []
        for line in f:
            players.append(line.strip())
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for player in players:
        markup.add(player)

    
    end = types.InlineKeyboardButton("End game!", callback_data='burningBridgesEnd')

    bot.send_message(int(player), "Your question is :" + qn)