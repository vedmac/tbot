import os

import psycopg2
from psycopg2 import sql

SERVER = os.getenv('POSTGRES_SERVER')
PORT = os.getenv('POSTGRES_PORT')
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DB')

con = psycopg2.connect(dbname='postgres', host=SERVER,
                       user=USER, password=PASSWORD, port=PORT)
con.autocommit = True
cur = con.cursor()
# sql.SQL and sql.Identifier are needed to avoid SQL injection attacks.
cur.execute(sql.SQL('CREATE DATABASE {};').format(sql.Identifier(DB)))
