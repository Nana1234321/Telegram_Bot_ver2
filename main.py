import telebot
import wikipedia
import re
import random
# Создаем экземпляр бота
bot = telebot.TeleBot('5876406321:AAEdHm9VeMXITuoNdYAL3OGiVF6Hmz3ttYU')
# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")
# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
cache = dict()


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext = ny.content[:1000]
        # Разделяем по точкам
        wikimas = wikitext.split('.')
        # Отбрасываем всёё после последней точки
        wikimas = wikimas[:-1]
        # создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not ('==' in x):
                # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if (len((x.strip())) > 3):
                    wikitext2 = wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'
# Функция, обрабатывающая команду /start


@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("🎲Рандомное число")
    item2 = telebot.types.KeyboardButton("🙃Как дела?")
    markup.add(item1, item2)

    bot.send_message(
        m.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipediaа')
# Получение сообщений от юзера


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == '🎲Рандомное число':
        bot.send_message(message.chat.id, str(random.randint(0, 100)))
    elif message.text == '🙃Как дела?':
        bot.send_message(message.chat.id, 'Отлично, сам как?')
    elif message.text not in cache:
        s = getwiki(message.text)
        bot.send_message(message.chat.id, "from wiki")
        bot.send_message(message.chat.id, s)
        cache[message.text] = s
    else:
        bot.send_message(message.chat.id, cache.get(message.text, 0))


# Запускаем бота
bot.polling(none_stop=True, interval=0)
