import os
import time

import scraper as amz
import telegram
from dotenv import load_dotenv
from models import Product

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT = telegram.Bot(token=TELEGRAM_TOKEN)
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = "https://www.amazon.com/Pampers-Training-Underwear-5t-6t-Count/dp/B01M2CZBCD/ref=sr_1_3?crid=KSTW33I9DL74&dchild=1&keywords=pampers+easy+ups+5t-6t&qid=1626787064&sprefix=pampers+ea%2Caps%2C195&sr=8-3"  # noqa


def get_amazone_data(url):
    """
    Get data from Amazon.
    """
    soup = amz.get_soup(url)
    title = amz.get_title(soup)
    price = amz.get_price(soup)
    availability = amz.get_availability(soup)
    return title, price, availability


def add_product(url):
    """
    Create a product in the database.
    """
    exists = Product.select().where(Product.url_field == url)
    if bool(exists):
        product = Product.get(Product.url_field == url)
        print(f"Product already exists: {product.title}")
    else:
        title, price, availability = get_amazone_data(url)
        product = Product.create(
            title=title,
            price=price,
            availability=availability,
            url_field=url,
        )
        product.save()
        return f"Product added: {title}"


def update_product(id):
    """
    Update a product in the database.
    """
    exists = Product.select().where(Product.id == id)
    if bool(exists):
        product = Product.get(Product.id == id)
        product.title, product.price, product.availability = get_amazone_data(
            product.url_field)
        product.save()
        # print(f"Product updated: {product.title}")
        # BOT.send_message(chat_id=CHAT_ID, text=f"{product.title} updated")
    # else:
    #     print(f"Product doesn't exist: {id}")
        # BOT.send_message(chat_id=CHAT_ID, text=f"{id} doesn't exist")


def remove_product(id):
    """
    Remove a product from the database.
    """
    exists = Product.select().where(Product.id == id)
    if bool(exists):
        product = Product.get(Product.id == id)
        product.delete_instance()
        # print(f"Product deleted: {product.title}")
        BOT.send_message(chat_id=CHAT_ID, text=f"{product.title} deleted")
    else:
        # print(f"Product doesn't exist: {id}")
        BOT.send_message(chat_id=CHAT_ID, text=f"{id} doesn't exist")


def get_all_products():
    """
    Get all products from the database.
    """
    products = Product.select()
    return products


def check_update():
    """
    Check if a product is updated.
    """
    for product in Product.select():
        title, price, availability = get_amazone_data(product.url_field)
        if product.availability != availability:
            update_product(product.id)
            BOT.send_message(chat_id=CHAT_ID, text=f"Availability {product.title} updated to {availability}")  # noqa
        elif product.price != price:
            BOT.send_message(chat_id=CHAT_ID, text=f"Price {product.title} updated from {product.price} to {price}")  # noqa
            update_product(product.id)
        elif product.title != title:
            update_product(product.id)
            BOT.send_message(chat_id=CHAT_ID, text=f"Title updated to {title}")
        else:
            BOT.send_message(chat_id=CHAT_ID, text="Nothing new")
        time.sleep(30)


if __name__ == "__main__":
    # new_product = get_amazone_data(URL)
    get_all_products()
    # check_update()
    # pampers = Product(title=new_product[0], price=new_product[1], availability=new_product[2], url_field=URL)  # noqa
    # pampers.save()
    # create_product("https://www.amazon.com/Pampers-Training-Underwear-5t-6t-Count/dp/B01M2CZBCD/ref=sr_1_3?crid=KSTW33I9DL74&dchild=1&keywords=pampers+easy+ups+5t-6t&qid=1626787064&sprefix=pampers+ea%2Caps%2C195&sr=8-3")
    # for produst in Product.select():
    #     print(produst.title, '\n', produst.availability,
    #         '\n', produst.price, '\n', produst.url_field)
    #     print(type(produst.id))
    # BOT.send_message(chat_id=CHAT_ID, text=produst.title)
    # BOT.send_message(chat_id=CHAT_ID, text=produst.availability)
