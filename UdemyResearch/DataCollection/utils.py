import time
import random


def sleep_randomly():
    random_sleep = random.randint(10, 20)
    time.sleep(random_sleep)


def get_mongo_collection(client, db_name, col_name):
    db = client[db_name]
    col = db[col_name]
    return col
