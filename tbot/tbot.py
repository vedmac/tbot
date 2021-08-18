import logging
import os
from time import sleep

import telegram
from dotenv import load_dotenv
from operations import (add_product, check_update, get_all_products,
                        remove_product)
from telegram.ext import CommandHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
                    level=logging.INFO)

load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT = telegram.Bot(token=TELEGRAM_TOKEN)
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# получаем экземпляр `Updater`
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
# получаем экземпляр `Dispatcher`
dispatcher = updater.dispatcher


def get_all(update, context):
    """
    Функция для отправки всех товаров в консоль
    :param update:
    :param context:
    :return:
    """
    context.bot.send_message(chat_id=CHAT_ID, text="Все товары:")
    get_all_products()


def add(update, context):
    if context.args:
        url = context.args[0]
        add_product(url)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No command url')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='send: /add url')


def remove(update, context):
    if context.args:
        id = context.args[0]
        remove_product(id)


def check(update, context):
    check_update()


def updeter(update, context):
    while context.args[0] != 'stop':
        check_update()
        sleep(24 * 60 * 60)
    context.bot.send_message(chat_id=CHAT_ID, text="Autoupdater stopped")

updater_handler = CommandHandler('updater', updeter)
dispatcher.add_handler(updater_handler)
check_handler = CommandHandler('check', check)
dispatcher.add_handler(check_handler)
remove_handler = CommandHandler('remove', remove)
dispatcher.add_handler(remove_handler)
add_handler = CommandHandler('add', add)
dispatcher.add_handler(add_handler)
get_all_handler = CommandHandler('get_all', get_all)
dispatcher.add_handler(get_all_handler)


def start():
    # запуск прослушивания сообщений
    updater.start_polling()
    # обработчик нажатия Ctrl+C
    updater.idle()
