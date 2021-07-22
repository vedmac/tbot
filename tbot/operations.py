import peewee
from model import *


if __name__ == '__main__':
    try:
        db.connect()
        Product.create_table()
    except peewee.InternalError as px:
        print(str(px))
