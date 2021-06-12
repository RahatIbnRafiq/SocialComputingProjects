from selenium import webdriver
import constants
import time
import random


def sleep_randomly():
    random_sleep = random.randint(10, 20)
    time.sleep(random_sleep)


def interview_discover():
    options = webdriver.ChromeOptions()
    options.headless = True
    page_count = 1
    f = open("interview_links.txt", "w")
    links_collected_so_far = 0
    while True:
        try:
            interview_url = constants.INTERVIEW_URL_ADDRESS + str(page_count)
            print("Collecting data for url: " + interview_url)
            driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
            driver.get(interview_url)
            sleep_randomly()
            containers = driver.find_elements_by_class_name('interviews__interview')
            links_collected_so_far += len(containers)
            for item in containers:
                link_element = item.find_element_by_class_name("interview__link")
                link = link_element.get_attribute('href')
                link = link.strip()
                f.write(link + "\n")
            page_count += 1
            print("Interview links collected so far: " + str(links_collected_so_far))
        except Exception as e:
            print(e)
            break
    f.close()


interview_discover()
