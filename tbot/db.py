from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from models import Product
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///prodacts.db")
if not database_exists(engine.url):
    create_database(engine.url)
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
for instance in session.query(Product).order_by(Product.id):
    print(instance.title, instance.price)
# vasiaProdact = Product("pampers", "$10", "no")
# print(database_exists(engine.url))
# session.add(vasiaProdact)
# session.commit()
# print(vasiaProdact.id)

# print(engine)
