import telebot
from config import TOKEN
from extensions import Converter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_bot(message: telebot.types.Message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Помощь', 'Список валют')
    bot.send_message(message.chat.id, text=get_text_help(), reply_markup=keyboard)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text, keyboard = get_page_symbols(page=0)
    bot.send_message(message.chat.id, text=text, reply_markup=keyboard)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    if message.text.lower() == 'помощь':
        bot.send_message(message.chat.id, text=get_text_help())
    elif message.text.lower() == 'список валют':
        text, keyboard = get_page_symbols(page=0)
        bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
    else:
        try:
            arguments = message.text.split(' ')
            arguments = [item for item in arguments if item]
            if len(arguments) != 3:
                raise APIException('Введи две валюты через пробел и количество. Подробнее /help')
            quote, base, amount = arguments
            quote = quote.lower()
            base = base.lower()
            price, quote, base = Converter.get_price(quote, base, amount)
        except APIException as e:
            bot.reply_to(message, f'{message.from_user.first_name} {message.from_user.last_name}, повнимательнее!\n{e}')
        except Exception as e:
            bot.reply_to(message, f'Ошибка на сервере!\n{e} Попробуйте повторить попытку позже.')
        else:
            text = f'{amount} {quote} = {price} {base}'
            bot.send_message(message.chat.id, text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.isdigit():
        page = int(call.data)
        text, keyboard = get_page_symbols(page=page)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=keyboard)


def get_text_help():
    return 'Чтобы начать работу введите команду бота в следующем формате:\n <имя валюты> \
        <в какую валюту перевести> <количество переводимой валюты>\nУвидеть свисок всех достпных валют: /values'


def get_page_symbols(page=0, max_symbols=20):
    symbols = sorted(Converter.get_symbols().items())
    number_symbols = len(symbols)
    start = page * max_symbols
    if number_symbols < start + max_symbols:
        symbols = symbols[start:]
    else:
        symbols = symbols[start:start+max_symbols]
    text = 'Доступные валюты:'
    for key, value in symbols:
        symbol = ' - '.join((key, value))
        text = '\n'.join((text, symbol))

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    buttons = []
    for n in range(0, (number_symbols//max_symbols)+1):
        if n != page:
            buttons.append(telebot.types.InlineKeyboardButton(text=f"{n+1}", callback_data=f"{n}"))
    keyboard.add(*buttons)
    return [text, keyboard]


bot.polling()
