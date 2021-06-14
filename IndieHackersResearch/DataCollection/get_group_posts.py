from selenium import webdriver
import constants
import time
import random
from selenium.common.exceptions import NoSuchElementException
import sys


def sleep_randomly():
    random_sleep = random.randint(5, 10)
    time.sleep(random_sleep)

def get_all_group_links():
    group_links = []
    f = open("group_links.txt", "r")
    for line in f:
        group_links.append(line.strip())
    f.close()
    return group_links


def group_posts(start, end):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920,1080")
    group_links = get_all_group_links()
    for i in range(start, end):
        f = open("groups_" + str(i)+".txt", "w")
        post_dict = dict()
        group_link = group_links[i]
        print("-------------------------------------------------------")
        print("Collecting posts for group: " + str(group_link))
        driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
        driver.maximize_window()
        driver.get(group_link)
        sleep_randomly()
        about_list = []
        try:
            group_index_sidebar = driver.find_element_by_class_name("group-index__sidebar")
            abouts = group_index_sidebar.find_elements_by_class_name("group-index__about-section")
            for about in abouts:
                about_text = about.text.strip().replace("\n", ",")
                about_list.append(about_text)
        except Exception as e:
            print("Exception when getting the about section info: " + str(e))
        post_links = set()
        discussions = []
        while True:
            try:
                discussions_html = driver.find_element_by_class_name("group-index__discussions")
                discussions = discussions_html.\
                    find_elements_by_css_selector("div.feed-item.feed-item--compact.feed-item--post.feed-item--post-in-group.ember-view")
                print("posts: " + str(len(discussions)))
                count = 100
                while count:
                    driver.execute_script('window.scrollTo(0, 100*document.body.scrollHeight);')
                    cur_height = driver.execute_script("return document.body.scrollHeight")
                    print("cur_height : " + str(cur_height) + " count is : " + str(count))
                    count -= 1
                print("Lets find the load more button")
                load_more = discussions_html.find_element_by_css_selector("button.soc-fd__more-button.load-more-button.ember-view")
                driver.execute_script("arguments[0].scrollIntoView();", load_more)
                load_more.click()
                print("Going to sleep now")
                sleep_randomly()
                print("-------------------------------------------------------")
            except NoSuchElementException as e:
                print("Collected all posts.Load more button not found! " + str(e))
                break
            except Exception as e:
                print("Exception happened!!!  " + str(e))

        discussions_html = driver.find_element_by_class_name("group-index__discussions")
        discussions = discussions_html. \
            find_elements_by_css_selector(
            "div.feed-item.feed-item--compact.feed-item--post.feed-item--post-in-group.ember-view")
        for discussion in discussions:
            discussion_link_element = discussion.find_element_by_css_selector("a.ember-view.feed-item__title-link")
            post_link = discussion_link_element.get_attribute('href')
            post_links.add(post_link.strip())
        driver.quit()
        print("Total posts collected : " + str(len(post_links)))
        print("-------------------------------------------------------")
        post_dict["group"] = group_link
        post_dict["posts"] = list(post_links)
        post_dict["about"] = list(about_list)
        f.write(str(post_dict) + "\n")
        f.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("You need two arguments to run this script. start and end index for the group_links file")
    else:
        start, end = int(sys.argv[1]), int(sys.argv[2])
        group_posts(start, end)
