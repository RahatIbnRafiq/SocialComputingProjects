from selenium import webdriver
import constants
import time
import random
import pickle
from os import listdir
from os.path import isfile, join
import pymongo

client = pymongo.MongoClient()


def get_mongo_collection(db_name, col_name):

    db = client[db_name]
    col = db[col_name]
    return col


def get_element(element, css_selector):
    try:
        e = element.find_element_by_css_selector(css_selector)
        return e
    except Exception:
        return None


def sleep_randomly():
    random_sleep = random.randint(3, 5)
    time.sleep(random_sleep)


def get_all_courses():
    all_courses = []
    f = open("all_course_links.txt", "r")
    for line in f:
        all_courses.append(line.strip())
    f.close()
    count = 0
    for i in range(len(all_courses)):
        print("-------------------------------------------------")
        course = scrape_webpage(all_courses[i], i)
        count += 1
        with open("course_categories_" + str(i) + '.pickle', 'wb') as handle:
            pickle.dump(course, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("Total courses collected till now : {}".format(count))
        print("-------------------------------------------------")


def scrape_webpage(url, i):
    course = dict()
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
    course["url"] = url
    print(url)

    try:
        driver.maximize_window()
        driver.get(url)
        sleep_randomly()
        try:
            element = driver.find_element_by_css_selector("div.topic-menu.udlite-breadcrumb")
            elements =\
                element.find_elements_by_css_selector("a.udlite-heading-sm")
            categories = []
            for i in range(0, len(elements)):
                categories.append(elements[i].text)
            print("Collecting course category for course: {}".format(i, url))
            print("categories are : ")
            print(categories)
            course["categories"] = categories
            print("---------------------------------------------------")
        except Exception as e:
            print(e)
    finally:
        driver.quit()
        return course


def get_all_files(location):
    files = [f for f in listdir(location) if isfile(join(location, f))]
    return files


def insert_to_db():
    location = "/Users/rahatibnrafiq/MyWorkSpace/SocialComputingProjects/UdemyResearch/DataCollection/"
    filenames = get_all_files(location)
    course_details_collection = get_mongo_collection("udemy", "course_categories")
    for filename in filenames:
        if "pickle" not in filename:
            continue
        with open(location+filename, 'rb') as handle:
            try:
                course = pickle.load(handle)
                course_details_collection.insert_one(course)
            except Exception as e:
                print("Exception happened: ", filename, e, b)
                break


if __name__ == "__main__":
    get_all_courses()
    # insert_to_db()
