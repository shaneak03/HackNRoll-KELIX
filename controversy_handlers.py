import telebot
import random

questions = [
    "Is pineapple on pizza acceptable? 🍍🍕",
    "Should toilet paper hang over or under? 🧻",
    "Is a hotdog a sandwich? 🌭",
    "Is cereal a soup? 🥣",
    "Should you put ketchup on a hotdog? 🌭🍅",
    "Is it okay to wear socks with sandals? 🧦👡",
    "Is it better to be early or late? ⏰",
    "Should you shower in the morning or at night? 🚿",
    "Is it okay to double-dip at a party? 🍴",
    "Is it better to work from home or in an office? 🏠🏢"
]

def start_controversy(bot: telebot.TeleBot, message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        poll_question = random.choice(questions)
        create_poll(bot, message, poll_question)
    else:
        bot.reply_to(message, "👾 Please use this command in a group or supergroup. 👾")

def create_poll(bot, message, poll_question):
    bot.send_poll(
        chat_id=message.chat.id,
        question=poll_question,
        options=["Yes/Former", "No/Latter"],
        is_anonymous=False
    )