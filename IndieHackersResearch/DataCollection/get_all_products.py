from selenium import webdriver
import constants
import time
import random
from selenium.common.exceptions import NoSuchElementException
import sys


def element_exists(html, element):
    try:
        html.find_element_by_css_selector(element)
        return True
    except Exception:
        return False


def sleep_randomly():
    random_sleep = random.randint(5, 10)
    time.sleep(random_sleep)


def get_all_products(max, min):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=YouKnowWho")

    try:
        driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
        driver.maximize_window()
        login(driver)
        minRevenue = min
        maxRevenue = 0
        while maxRevenue <= max:
            maxRevenue = minRevenue + 10000
            ALL_PRODUCTS_URL =\
                "https://www.indiehackers.com/products?maxRevenue="+str(maxRevenue)+"&minRevenue="+str(minRevenue)
            print(ALL_PRODUCTS_URL)
            driver.get(ALL_PRODUCTS_URL)
            sleep_randomly()
            product_cards = []
            while element_exists(driver, "button.load-more-button.ember-view.products-index__load-more-button"):
                load_more_button =\
                    driver.find_element_by_class_name("load-more-button.ember-view.products-index__load-more-button")
                load_more_button.click()
                count = 50
                while count:
                    driver.execute_script('window.scrollTo(0, 50*document.body.scrollHeight);')
                    count -= 1
                    cur_height = driver.execute_script("return document.body.scrollHeight")
                    print("cur_height : " + str(cur_height) + " count is : " + str(count))
                    time.sleep(3)
                products_index_cards = driver.find_element_by_css_selector("div.products-index__content")
                product_cards = products_index_cards.find_elements_by_css_selector("div.product-card.ember-view")
                print("{} total product cards till now".format(len(product_cards)))
                print("----------------------------------------------------------")
            print("Final product count for this url: {}".format(len(product_cards)))
            f = open("all_product_links_final.txt", "a")
            for product_card in product_cards:
                product = product_card.find_element_by_css_selector("a.product-card__link.ember-view")
                f.write(product.get_attribute("href") + "\n")
            print("{} product cards written for this url".format(len(product_cards)))
            f.close()
            minRevenue = maxRevenue+1
        driver.quit()
    except Exception as e:
        print("Exception happened: " + str(e))
    finally:
        driver.quit()


def login(driver):
    driver.get("https://www.indiehackers.com/sign-in")
    sleep_randomly()
    email = driver.find_element_by_css_selector("input.pw-sign-in__field.pw-sign-in__field--email.ember-text-field.ember-view")
    password = driver.find_element_by_css_selector("input.pw-sign-in__field.pw-sign-in__field--password.ember-text-field.ember-view")
    sleep_randomly()
    email.send_keys('rahatibnrafiq@gmail.com')
    sleep_randomly()
    password.send_keys("MAldIni089")
    sleep_randomly()
    sign_in_button = driver.find_element_by_css_selector("button.pw-sign-in__button")
    sign_in_button.click()
    sleep_randomly()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("You need two arguments to run this script. max revenue and min revenue")
    else:
        min, max = int(sys.argv[1]), int(sys.argv[2])
        get_all_products(max, min)

