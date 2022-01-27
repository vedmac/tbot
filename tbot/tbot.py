import logging
import os
import time

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from operations import (add_product, get_all_products, get_amazone_data,
                        remove_product, update_product)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
                    level=logging.INFO)

load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


if not TELEGRAM_TOKEN:
    exit("Error: no token provided")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="get_all")
async def cmd_get_all(message: types.Message):
    await message.answer("Все товары:")
    products = get_all_products()
    for product in products:
        text = f"{product.id} - {product.title} - {product.price} - {product.availability}"  # noqa
        # print(text)
        await message.answer(text)


@dp.message_handler(commands="check")
async def cmd_check(message: types.Message):
    products = get_all_products()
    for product in products:
        title, price, availability = get_amazone_data(product.url_field)
        if product.availability != availability:
            update_product(product.id)
            await message.answer(f"Availability {product.title} updated to {availability}")  # noqa
        elif product.price != price:
            await message.answer(f"Price {product.title} updated from {product.price} to {price}")  # noqa
            update_product(product.id)
        elif product.title != title:
            update_product(product.id)
            await message.answer(f"Title updated to {title}")
        else:
            await message.answer("Nothing new")
        time.sleep(30)


@dp.message_handler(commands="add")
async def cmd_add(message: types.Message):
    if message.get_args():
        url = message.get_args()
        text = add_product(url)
        await message.answer(text)
    else:
        await message.answer("Не указан url")


@dp.message_handler(commands="remove")
async def cmd_remove(message: types.Message):
    if message.get_args():
        id = message.get_args()
        remove_product(id)
        await message.answer(f"Удален товар {id}")
    else:
        await message.answer("Не указан id")


def start():
    executor.start_polling(dp, skip_updates=True)
