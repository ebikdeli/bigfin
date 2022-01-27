import sqlite3
from sqlite3.dbapi2 import OperationalError
import redis
from redis import exceptions
from datetime import datetime


# Setup redis connection and object: #
try:
    red = redis.Redis(host='127.0.0.1', port=6379, db=0)
    red.ping()
except (exceptions.ConnectionError, exceptions.TimeoutError):
    print('No connection made...')
    quit()
# Connect to database: #
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
try:
    data = cur.execute('SELECT id FROM currency')
except OperationalError:
    sql = """CREATE TABLE currency(
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                name varchar(100) NOT NULL,
                symbol varchar(10),
                price Decimal(17,10) DEFAULT 0,
                time DATETIME,
                founded varchar(4),
                is_crypto bool DEFAULT 0
            );"""
    cur.execute(sql)
    print('currency_currency created')
# Flush data from redis to database: #
currencies = ['bitcoin', 'ethereum', 'dogecoin']
# Convert 'bytes' to 'str': #
def convert(byt):
    return byt.decode()
k = red.keys()
keys = list(map(convert, k))
# Put data into database: #
for c in currencies:
    if c in keys:
        sql = """INSERT INTO currency (name, symbol, price, time, is_crypto)
                 VALUES(?, ?, ?, ?, ?);"""
        cur.execute(sql,
                   (c,
                    red.lindex(c, 2).decode(),
                    red.lindex(c, 1).decode(),
                    datetime.now(),
                    True))
conn.commit()
conn.close()
