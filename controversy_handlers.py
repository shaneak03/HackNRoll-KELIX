import telebot

def register_controversy_handlers(bot: telebot.TeleBot):
    @bot.message_handler(commands=['startControversy'])
    def start_controversy(message):
        if message.chat.type == 'group' or message.chat.type == 'supergroup':
            msg = bot.reply_to(message, "Please provide the question for the controversy poll.")
            bot.register_next_step_handler(msg, get_poll_question)
        else:
            bot.reply_to(message, "Please use this command in a group or supergroup.")

    def get_poll_question(message):
        poll_question = message.text
        msg = bot.reply_to(message, "Please provide the first option for the controversy poll.")
        bot.register_next_step_handler(msg, lambda m: get_first_option(m, poll_question))

    def get_first_option(message, poll_question):
        first_option = message.text
        msg = bot.reply_to(message, "Please provide the second option for the controversy poll.")
        bot.register_next_step_handler(msg, lambda m: get_second_option(m, poll_question, first_option))

    def get_second_option(message, poll_question, first_option):
        second_option = message.text
        create_poll(message, poll_question, first_option, second_option)

    def create_poll(message, poll_question, first_option, second_option):
        bot.send_poll(
            chat_id=message.chat.id,
            question=poll_question,
            options=[first_option, second_option],
            is_anonymous=False
        )