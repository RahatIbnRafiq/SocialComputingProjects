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


def get_user_followers(driver):
    followers_set = set()
    user_followers = driver.find_element_by_css_selector("span.user-stats__label")
    user_followers.click()
    sleep_randomly()
    user_followers = driver.find_element_by_css_selector("section.user-sidebar__section.user-followers")
    followers = user_followers.find_elements_by_css_selector("div.user-link.users-list__user-link.ember-view")
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
    return followers_set


def get_user_followings(driver):
    following_set = set()
    user_following = driver.find_element_by_css_selector("section.user-sidebar__section.user-following")
    followings = user_following.find_elements_by_css_selector("div.user-link.users-list__user-link.ember-view")
    while check_if_exists(user_following, "div.users-list__more-button"):
        followings = user_following.find_elements_by_css_selector("div.user-link.users-list__user-link.ember-view")
        more_following_button = user_following.find_element_by_css_selector("div.users-list__more-button")
        more_following_button.click()
        driver.execute_script('window.scrollTo(0, 100*document.body.scrollHeight);')
        time.sleep(2)
    for following in followings:
        username = following.find_element_by_css_selector("span.user-link__name.user-link__name--username")
        username = username.get_attribute("innerHTML").strip()
        following_set.add(username)
    return following_set


def get_user_data(username):
    # followers_set = set()
    options = webdriver.ChromeOptions()
    options.headless = True
    USER_URL = "https://www.indiehackers.com/"+username
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
    all_users = set()
    try:
        driver.maximize_window()
        print(USER_URL)
        driver.get(USER_URL)
        sleep_randomly()
        followers = get_user_followers(driver)
        for user in followers:
            all_users.add(user)
        followings = get_user_followings(driver)
        for user in followings:
            all_users.add(user)

        # d = dict()
        # d["username"] = username
        # d["followers"] = list(followers)
        # d["followings"] = list(followings)
        # user_network_collection = get_mongo_collection("indie_hackers", "user_networks")
        # user_network_collection.insert_one(d)
        return all_users
    except Exception as e:
        print("Exception in get user data: "+str(e))
    finally:
        sleep_randomly()
        driver.quit()
        return all_users

def get_users():
    try:
        users_set = set()
        # usernames_collection = get_mongo_collection("indie_hackers", "usernames")
        # users = usernames_collection.find({})
        # for user in users:
        #     users_set.add(user['username'])
        f = open("all_users.txt", "r")
        for line in f:
            users_set.add(line.strip())
        f.close()
        print(len(users_set))
        done_users = set()

        # f = open("all_users.txt", "w")
        # for user in users_set:
        #     f.write(str(user) + "\n")
        # f.close()
        while len(users_set) > 0:
            cur_user = users_set.pop()
            all_users = get_user_data(cur_user)
            f = open("all_users.txt", "a")
            for user in all_users:
                if user not in users_set:
                    f.write(str(user) + "\n")
                users_set.add(user)
            f.close()
            g = open("done_users.txt", "a")
            g.write(cur_user+"\n")
            g.close()
            done_users.add(cur_user)

            print("{} total users collected, {} total users remaining".format(len(done_users), len(users_set)))
    except Exception as e:
        print("Exception took place {}".format(e))
        pass




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
