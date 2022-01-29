import scraper as amz
from dotenv import load_dotenv
from models import Product

load_dotenv()


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
        return f"Product already exists: {product.title}"
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


def remove_product(id):
    """
    Remove a product from the database.
    """
    exists = Product.select().where(Product.id == id)
    if bool(exists):
        product = Product.get(Product.id == id)
        product.delete_instance()
        return f"{product.title} удален"
    else:
        return f"{id} такого товара нет"


def get_all_products():
    """
    Get all products from the database.
    """
    products = Product.select()
    return products


# def check_update():
#     """
#     Check if a product is updated.
#     """
#     for product in Product.select():
#         title, price, availability = get_amazone_data(product.url_field)
#         if product.availability != availability or product.price != price or product.title != title:  # noqa
#             BOT.send_message(chat_id=CHAT_ID, text=f"Product {product.title} - {product.price} - {product.availability} updated to {title} - {price} - {availability}")  # noqa
#             update_product(product.id)
#         else:
#             BOT.send_message(chat_id=CHAT_ID, text="Nothing new")
#         time.sleep(15)
