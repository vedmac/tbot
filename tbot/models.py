import os

from dotenv import load_dotenv
from peewee import (CharField, InternalError, Model, PostgresqlDatabase,
                    PrimaryKeyField)

load_dotenv()


SERVER = os.getenv('POSTGRES_SERVER')
PORT = os.getenv('POSTGRES_PORT')
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DB')


db = PostgresqlDatabase(DB, user=USER, password=PASSWORD,
                        host=SERVER, port=PORT)


class Product(Model):
    id = PrimaryKeyField(null=False)
    title = CharField(null=False)
    price = CharField()
    url_field = CharField(null=False, unique=True)
    availability = CharField()

    class Meta:
        db_table = "products"
        database = db  # модель будет использовать базу данных 'people.db'


try:
    db.connect()
    db.create_tables([Product])
except InternalError as px:
    print(str(px))
