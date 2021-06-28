from selenium import webdriver
import constants
import time
import random
from selenium.common.exceptions import NoSuchElementException
import pymongo

client = pymongo.MongoClient()

def sleep_randomly():
    random_sleep = random.randint(5, 10)
    time.sleep(random_sleep)


def check_if_exists(element, css_selector):
    try:
        element.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True


def get_initial_users():
    options = webdriver.ChromeOptions()
    options.headless = True
    USER_URL = "https://www.indiehackers.com/csallen"
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
    try:
        driver.maximize_window()
        driver.get(USER_URL)
        sleep_randomly()
        user_followers = driver.find_element_by_css_selector("span.user-stats__label")
        user_followers.click()
        sleep_randomly()
        user_followers = driver.find_element_by_css_selector("section.user-sidebar__section.user-followers")

        while check_if_exists(user_followers, "div.users-list__more-button"):
            followers = user_followers.find_elements_by_css_selector("div.user-link.users-list__user-link.ember-view")
            print(len(followers))
            more_followers_button = user_followers.find_element_by_css_selector("div.users-list__more-button")
            more_followers_button.click()
            driver.execute_script('window.scrollTo(0, 100*document.body.scrollHeight);')
            time.sleep(2)

        f = open("initial_users.txt", "w")
        for follower in followers:
            username = follower.find_element_by_css_selector("span.user-link__name.user-link__name--username")
            username = username.get_attribute("innerHTML").strip()
            f.write(username+"\n")
    except Exception as e:
        print(e)
    finally:
        sleep_randomly()
        driver.quit()
        f.close()



def get_user_followers(username):
    followers_set = ()
    options = webdriver.ChromeOptions()
    options.headless = True
    USER_URL = "https://www.indiehackers.com/"+username
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
    try:
        driver.maximize_window()
        driver.get(USER_URL)
        sleep_randomly()
        user_followers = driver.find_element_by_css_selector("span.user-stats__label")
        user_followers.click()
        sleep_randomly()
        user_followers = driver.find_element_by_css_selector("section.user-sidebar__section.user-followers")
        while check_if_exists(user_followers, "div.users-list__more-button"):
            followers = user_followers.find_elements_by_css_selector("div.user-link.users-list__user-link.ember-view")
            more_followers_button = user_followers.find_element_by_css_selector("div.users-list__more-button")
            more_followers_button.click()
            driver.execute_script('window.scrollTo(0, 100*document.body.scrollHeight);')
            time.sleep(2)
        for follower in followers:
            username = follower.find_element_by_css_selector("span.user-link__name.user-link__name--username")
            username = username.get_attribute("innerHTML").strip()
            followers_set.add(username)
    except Exception as e:
        print(e)
    finally:
        sleep_randomly()
        driver.quit()

def get_users():
    users_set = set()
    usernames_collection = get_mongo_collection("indie_hackers", "usernames")
    users = usernames_collection.find({})
    for user in users:
        users_set.add(user['username'])
    print(len(users_set))

    while len(users_set) > 0:
        cur_user = users_set.pop()



def get_mongo_collection(db_name, col_name):
    db = client[db_name]
    col = db[col_name]
    return col


def insert_initial_users_to_db():
    with open("initial_users.txt") as f:
        lines = f.readlines()
        for line in lines:
            username = line.strip()
            usernames_collection = get_mongo_collection("indie_hackers", "usernames")
            usernames_collection.insert_one({'username': username})


# insert_initial_users_to_db()
# get_initial_users()
get_users()
client.close()
