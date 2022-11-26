import telebot
import config
import pathlib
import random


currpath = pathlib.Path(__file__).parent.resolve()

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open(str(currpath) + '/Images/hi.webp', 'rb')  # download sticker

    # keyboard
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("🎲Рандомное число")
    item2 = telebot.types.KeyboardButton("🙃Как дела?")
    markup.add(item1, item2)

    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n Я - <b>{1.first_name}</b>, бот - подопытный кроль\n Могу назвать рандомное число \n",
                     "Можем сыграть в игру".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)  # вариант разметки


@bot.callback_query_handler(func=lambda callback_query: callback_query.game_short_name == 'simplegame')
def game(call):
    bot.answer_callback_query(
        callback_query_id=call.id, url='https://agar.io/#ffa')


if __name__ == "main":
    bot.polling()


@bot.message_handler(content_types=['text'])
def Blabla(message):
    if message.chat.type == 'private':
        if message.text == '🎲Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == '🙃Как дела?':
            bot.send_message(message.chat.id, 'Отлично, сам как?')
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить🙁')


# RUN
bot.polling(non_stop=True)
