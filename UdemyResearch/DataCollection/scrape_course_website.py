from selenium import webdriver
import constants
import time
import random
import pickle
import sys


def get_element(element, css_selector):
    try:
        e = element.find_element_by_css_selector(css_selector)
        return e
    except Exception:
        return None


def sleep_randomly():
    random_sleep = random.randint(5, 10)
    time.sleep(random_sleep)


def get_all_courses(start, end):
    all_courses = []
    f = open("all_course_links.txt", "r")
    for line in f:
        all_courses.append(line.strip())
    f.close()
    count = 0
    for i in range(start, end):
        print("-------------------------------------------------")
        course = scrape_webpage(all_courses[i], i)
        count += 1
        with open("course_detail_" + str(i) + '.pickle', 'wb') as handle:
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
    print("Value of i is {}, Collecting course data for course: {}".format(i, url))
    try:
        driver.maximize_window()
        driver.get(url)
        sleep_randomly()
        try:
            elements = driver.find_elements_by_css_selector("div.course-landing-page__main-content.dark-background-inner-text-container")
            badge_element = None
            meta_element = None
            for i in range(0, len(elements)):
                e = get_element(elements[i], "div.clp-lead__badge-ratings-enrollment")
                if e is not None and badge_element is None:
                    badge_element = elements[i]
                e = get_element(elements[i], "div.clp-lead__element-meta")
                if e is not None and meta_element is None:
                    meta_element = elements[i]

            if badge_element:
                items = badge_element.find_elements_by_css_selector("div.clp-component-render")
                for item in items:
                    item_text = item.text.strip()
                    if "out of" in item_text:
                        course["rating"] = item_text
                    elif "ratings)" in item_text:
                        course["num_ratings"] = item_text
                    elif "students" in item_text:
                        course["num_students"] = item_text
            if meta_element:
                e = get_element(meta_element, "div.clp-lead__element-item.clp-lead__locale")
                if e is not None:
                    course["locale"] = e.text

                e = get_element(meta_element, "div.ud-component--course-landing-page-udlite--caption")
                if e is not None:
                    course["captions"] = e.get_attribute("data-component-props")

            try:
                sidebar_element = driver.find_element_by_css_selector("div.generic-purchase-section--ctas--1wqHF")
                course["sidebar_info"] = sidebar_element.text.strip()
            except Exception as e:
                print(e)

            try:
                instructor_element = driver.find_element_by_css_selector("div.ud-component--course-landing-page-udlite--instructors")
                course["instructor_info"] = instructor_element.get_attribute("data-component-props").strip()
            except Exception as e:
                print(e)

        except Exception as e:
            print(e)
    finally:
        driver.quit()
        return course


def read_pickle_files(start, end):
    for i in range(start, end):
        with open('course_detail_'+str(i)+'.pickle', 'rb') as handle:
            b = pickle.load(handle)
            print(b)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("You need two arguments to run this script. start and end index for the course links file")
    else:
        start, end = int(sys.argv[1]), int(sys.argv[2])
        get_all_courses(start, end)
        # read_pickle_files(start, end)
