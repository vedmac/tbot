from peewee import (CharField, InternalError, Model, PrimaryKeyField,
                    SqliteDatabase)

db = SqliteDatabase('products.db')


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
    Product.create_table()
except InternalError as px:
    print(str(px))
