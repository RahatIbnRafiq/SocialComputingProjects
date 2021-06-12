import time
import random


def sleep_randomly():
    random_sleep = random.randint(10, 20)
    time.sleep(random_sleep)
