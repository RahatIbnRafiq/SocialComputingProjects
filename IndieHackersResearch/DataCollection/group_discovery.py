from selenium import webdriver
import constants
import time
import random
from selenium.common.exceptions import NoSuchElementException


def sleep_randomly():
    random_sleep = random.randint(10, 20)
    time.sleep(random_sleep)


def groups_discover():
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
    driver.get(constants.GROUP_LIST_URL)
    sleep_randomly()
    group_set = set()
    community_content = driver.find_element_by_class_name("community__group-lists")
    communities = community_content.find_elements_by_css_selector("div.group-list.ember-view.community__group-list")
    for community in communities:
        community_title = community.find_element_by_class_name("group-list__title").text
        print("-------------------------------------------------------")
        print("Community : " + community_title)
        try:
            while True:
                groups = community.find_elements_by_class_name("group-list__group")
                for group in groups:
                    group_link_element = group.find_element_by_css_selector("a.ember-view.group-list__group-link")
                    group_link = group_link_element.get_attribute('href')
                    group_link = group_link.strip()
                    group_set.add(group_link)
                show_more_button = community.find_element_by_class_name("group-list__more-button")
                show_more_button.click()
                sleep_randomly()
        except NoSuchElementException as e:
            print("Collected all groups. Show more button not found! " + str(e))
        except Exception as e:
            print(e)
        finally:
            print("Total groups collected so far: " + str(len(group_set)))
            print("-------------------------------------------------------")
            sleep_randomly()
    f = open("group_links.txt", "a")
    for group in group_set:
        f.write(group.strip() + "\n")
    f.close()



groups_discover()
