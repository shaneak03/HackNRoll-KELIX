import telebot
import threading
from objects import Groups

questions = [
    "Never have I ever accidentally waved back at someone who wasn’t waving👋🏻 at me.",
    "Never have I ever walked into the wrong opposite gender's toilet😱.",
    "Never have I ever tripped over absolutely nothing🤨.",
    "Never have I ever sent a text to the wrong person😱.",
    "Never have I ever fallen asleep in class or during a meeting😴.",
    "Never have I ever gone bungee jumping or skydiving🪂.",
    "Never have I ever traveled to another country alone✈️.",
    "Never have I ever dropped food on the floor and still eaten it🍕.",
    "Never have I ever lied on my resume📝.",
    "Never have I ever dropped my phone in the toilet🚽.",
    "Never have I ever accidentally liked an old social media post while stalking someone📱.",
    "Never have I ever talked to myself in the mirror🪞.",
    "Never have I ever made up an excuse to get out of plans🙊.",
    "Never have I ever Googled myself out of curiosity🔍."
]

# Dictionary to track points for each user
user_points = {}
# Dictionary to map poll IDs to question indices
poll_id_to_question_index = {}
# Dictionary to map poll IDs to chat IDs
poll_id_to_chat_id = {}
# Dictionary to track if a poll has been answered
poll_answered = {}

def never_have_i_ever(bot: telebot.TeleBot, message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        bot.reply_to(message, "Starting 'Never Have I Ever' game!🔥🔥🔥")
        initialize_points(bot, message)
        ask_next_question(bot, message, 0)
    else:
        bot.reply_to(message, "👾Please use this command in a group or supergroup.👾")

def initialize_points(bot, message):
    chat_id = message.chat.id
    group = Groups(chat_id)
    group.pull_members()
    members = group.members_id
    user_points[chat_id] = {}
    for member_id in members:
        user_points[chat_id][member_id] = 10

def ask_next_question(bot, message, question_index):
    if question_index < len(questions):
        question = questions[question_index]
        poll_message = bot.send_poll(
            chat_id=message.chat.id,
            question=question,
            options=["Have", "Have Not"],
            is_anonymous=False,
            allows_multiple_answers=False,
            type='regular'
        )
        poll_id_to_question_index[poll_message.poll.id] = question_index
        poll_id_to_chat_id[poll_message.poll.id] = message.chat.id
        poll_answered[poll_message.poll.id] = False
        threading.Timer(5.0, close_poll, args=[bot, poll_message.poll.id, message.chat.id, question_index]).start()
    else:
        bot.send_message(message.chat.id, "🎉 Game over! Thanks for playing. 🎉")
        display_points(bot, message)

def close_poll(bot, poll_id, chat_id, question_index):
    if poll_id in poll_answered and not poll_answered[poll_id]:
        try:
            bot.stop_poll(chat_id, poll_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Failed to stop poll {poll_id}: {e}")
        for user_id in user_points[chat_id]:
            if user_points[chat_id][user_id] > 0:
                user_points[chat_id][user_id] -= 1
                if user_points[chat_id][user_id] == 0:
                    bot.send_message(chat_id, f"🚫 User {user_id} is eliminated! 🚫")
        ask_next_question_by_poll(bot, chat_id, question_index + 1)

def handle_poll_answer(bot, poll_answer):
    poll_id = poll_answer.poll_id
    user_id = poll_answer.user.id
    chat_id = poll_id_to_chat_id.get(poll_id)
    if chat_id is None:
        print(f"Poll ID {poll_id} not found in poll_id_to_chat_id")
        return
    if user_id not in user_points[chat_id]:
        user_points[chat_id][user_id] = 10  # Initialize points for the user if not already present
    if poll_answer.option_ids[0] == 0:  # "Have" is the first option
        user_points[chat_id][user_id] -= 1
        if user_points[chat_id][user_id] == 0:
            bot.send_message(chat_id, f"🚫 User {user_id} is eliminated! 🚫")
    if not poll_answered[poll_id]:
        poll_answered[poll_id] = True
        question_index = get_question_index(poll_id)
        # Ensure the next question is asked only after 30 seconds
        threading.Timer(5.0, ask_next_question_by_poll, args=[bot, chat_id, question_index + 1]).start()

def get_question_index(poll_id):
    return poll_id_to_question_index.get(poll_id, 0)

def ask_next_question_by_poll(bot, chat_id, question_index):
    # if question_index < len(questions):
    if question_index < 5:
        question = questions[question_index]
        poll_message = bot.send_poll(
            chat_id=chat_id,
            question=question,
            options=["Have", "Have Not"],
            is_anonymous=False,
            allows_multiple_answers=False,
            type='regular'
        )
        poll_id_to_question_index[poll_message.poll.id] = question_index
        poll_id_to_chat_id[poll_message.poll.id] = chat_id
        poll_answered[poll_message.poll.id] = False
        threading.Timer(5.0, close_poll, args=[bot, poll_message.poll.id, chat_id, question_index]).start()
    else:
        bot.send_message(chat_id, "🎉 Game over! Thanks for playing. 🎉")
        display_points_by_chat_id(bot, chat_id)

def display_points(bot, message):
    chat_id = message.chat.id
    display_points_by_chat_id(bot, chat_id)

def display_points_by_chat_id(bot, chat_id):
    points_message = "🏆 Final points:\n"
    for user_id, points in user_points[chat_id].items():
        user = bot.get_chat_member(chat_id, user_id).user
        points_message += f"{user.first_name}: {points} points\n"
    bot.send_message(chat_id, points_message)
