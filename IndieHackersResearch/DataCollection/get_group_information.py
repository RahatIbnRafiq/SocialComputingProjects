from selenium import webdriver
import constants
import time
import random
import pymongo
from selenium.common.exceptions import NoSuchElementException
import sys


def sleep_randomly():
    random_sleep = random.randint(10, 20)
    time.sleep(random_sleep)


def get_group_members(driver, tag, userSet):
    prev_count = 0
    try:
        while True:
            group_members_section = driver.find_element_by_css_selector(tag)
            group_members = group_members_section.find_elements_by_css_selector("div.user-link.user-list__user-link.ember-view")
            sleep_randomly()
            for member in group_members:
                try:
                    username = member.find_element_by_css_selector("span.user-link__name.user-link__name--username")
                    userSet.add(username.text.strip())
                except Exception:
                    break
            if prev_count == len(userSet):
                break
            prev_count = len(userSet)
            print("# of Group members collected so far : " + str(len(userSet)))
            load_more = group_members_section.find_element_by_css_selector("svg.user-list__load-icon.ember-view")
            load_more.click()
            sleep_randomly()
    except NoSuchElementException as e:
        print("Collected all group members. Load more button not found! " + str(e))
    except Exception as e:
        print("Exception happened!!!!" + str(e))
    finally:
        print("Total Group members collected : " + str(len(userSet)))
        sleep_randomly()
        return userSet


def get_group_information(start, end):
    # group_info_collection = get_mongo_collection("indie_hackers", "group_info")
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
    group_links = get_all_group_links()
    all_groups = []
    for i in range(start, end):
        f = open("group_" + str(i)+".txt", "w")
        group_link = group_links[i]
        print("-------------------------------------------------------")
        print("Collecting members for " + str(i) + " -th  group: " + group_link + " ")
        f.write("Group link: " + str(group_link) + "\n")
        driver.get(group_link + "/members")
        sleep_randomly()

        print("collecting moderators")
        moderators = get_group_members(driver, "section.group-members__section.group-members__section--admins", set())
        print("collecting members")
        members = get_group_members(driver, "section.group-members__section.group-members__section--members", set())

        group_info = dict()
        group_info["url"] = group_link
        group_info["moderators"] = list(moderators)
        group_info["members"] = list(members)
        f.write(str(group_info) + "\n")
        # print(group_info)
        # group_info_collection.insert_one(group_info)
        print("-------------------------------------------------------")
        f.close()
    return all_groups


def get_all_group_links():
    group_links = []
    f = open("group_links.txt", "r")
    for line in f:
        group_links.append(line.strip())
    f.close()
    return group_links


def get_mongo_collection(db_name, col_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    col = db[col_name]
    return col


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("You need two arguments to run this script. start and end index for the group_link file")
    else:
        start, end = int(sys.argv[1]), int(sys.argv[2])
        get_group_information(start, end)
