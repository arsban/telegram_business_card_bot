import os
import telegram
from telegram import message
from telegram.ext import CommandHandler, Updater, Filters, MessageHandler
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

logging.basicConfig(
    level=logging.DEBUG,
    filename='telegram_bot.log',
    datefmt='%Y-%m-%d, %H:%M:%S',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    filemode='w',
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler_rotate = RotatingFileHandler(
    'telegram_bot.log',
    maxBytes=50_000_000,
    backupCount=5,
)
handler_stream = logging.StreamHandler()
logger.addHandler(handler_rotate)
logger.addHandler(handler_stream)


bot = telegram.Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN)
dp = updater.dispatcher


COMAND_ANSWERS = {
    'start': (
        'Привет {}!'
        '\nЯ Python-разработчик и это мой Бот-визитка'
        '\nС моими работами можно ознакомиться нажав на кнопку "GitHub"'
        '\nМое резюме на hh.ru можно посмотреть нажав на кнопку "Resume"'
        '\nБолее подроную информацию про меня можно узнать на кнопку "Об Авторе"'
        ),
    'GitHub': 'https://github.com/arsban',
    'Resume': 'https://hh.ru/resume/272859cdff09730b0d0039ed1f354577334678',
    'Об Авторе': 'надо заполнить',
}


def send_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)


def text_message_controler(update, context):
    chat = update.effective_chat
    text_mesage = update.message.text
    if text_mesage == 'GitHub':
        context.bot.send_message(chat_id=chat.id, text=COMAND_ANSWERS['GitHub'])
    elif text_mesage == 'Resume':
        context.bot.send_message(chat_id=chat.id, text=COMAND_ANSWERS['Resume'])
    elif text_mesage == 'Об Авторе':
        context.bot.send_message(chat_id=chat.id, text=COMAND_ANSWERS['Об Авторе'])
    else:
        context.bot.send_message(chat_id=chat.id, text=f'Я не понимаю: {text_mesage} - не запрограмирован еще:(')


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([
        ['GitHub', 'Resume'],
        ['Об Авторе'],
    ])
    context.bot.send_message(chat_id=chat.id, text=COMAND_ANSWERS['start'].format(name), reply_markup=button)


################
# тут обрабатываются команды с "/" например "/start" и "/help"
dp.add_handler(CommandHandler('start', wake_up))
################
################
# тут обрабатываются текстовые сообщения (str) и разные типы файлов.
dp.add_handler(MessageHandler(Filters.text, text_message_controler))
################
# Метод start_polling() запускает процесс polling, 
# приложение начнёт отправлять регулярные запросы для получения обновлений.
# параметр poll_interval обозначает нужный интервал запросов (в секундах, float)
updater.start_polling(poll_interval=5.0)
################
# Бот будет работать до тех пор, пока не нажмете Ctrl-C
updater.idle()
################