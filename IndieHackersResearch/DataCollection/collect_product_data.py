from selenium import webdriver
import constants
import time
import random
import sys
import pickle


def element_exists(html, element):
    try:
        html.find_element_by_css_selector(element)
        return True
    except Exception:
        return False


def get_product_links():
    links = []
    f = open("all_product_links_final.txt", "r")
    for line in f:
        links.append(line.strip())
    print(len(links))
    links = list(set(links))
    links = sorted(links)
    print(len(links))
    return links


def sleep_randomly():
    random_sleep = random.randint(5, 10)
    time.sleep(random_sleep)


def get_followers(driver, product_url):
    followers_set = set()
    try:
        driver.get(product_url+"/followers")
        sleep_randomly()
        product_followers_content = driver.find_element_by_css_selector("div.product-followers__content")
        followers = product_followers_content.find_elements_by_css_selector("div.user-link.users-list__user-link.ember-view")
        while element_exists(product_followers_content, "div.users-list__more-button"):
            followers = product_followers_content.find_elements_by_css_selector("div.user-link.users-list__user-link.ember-view")
            more_followers_button = product_followers_content.find_element_by_css_selector("div.users-list__more-button")
            more_followers_button.click()
            driver.execute_script('window.scrollTo(0, 100*document.body.scrollHeight);')
            time.sleep(2)
        for follower in followers:
            username = follower.find_element_by_css_selector("span.user-link__name.user-link__name--username")
            username = username.get_attribute("innerHTML").strip()
            followers_set.add(username)
    except Exception as e:
        print("Exception happened when collecting followers for this product: " + str(e))
    print("Total followers collected : {}".format(len(followers_set)))
    return list(followers_set)


def get_updates(driver, product_url):
    update_cards = []
    loop_count = 0

    while loop_count < 3 and len(update_cards) == 0:
        if loop_count > 0:
            print("Something happened when trying to collect updates the first time. Trying again")
            driver.get(product_url)
            sleep_randomly()
            sleep_randomly()
            sleep_randomly()
        try:
            if element_exists(driver, "section.product-index__timeline"):
                product_update_content = driver.find_element_by_css_selector("section.product-index__timeline")
                update_cards = product_update_content.find_elements_by_css_selector("div.product-update__content")
            while element_exists(driver, "button.product-index__load-more-button.load-more-button.ember-view"):
                load_more_button = driver.find_element_by_class_name(
                    "product-index__load-more-button.load-more-button.ember-view")
                load_more_button.click()
                count = 15
                while count:
                    driver.execute_script('window.scrollTo(0, 50*document.body.scrollHeight);')
                    count -= 1
                sleep_randomly()

                product_index_timeline = driver.find_element_by_css_selector("section.product-index__timeline")
                update_cards = product_index_timeline.find_elements_by_css_selector("div.product-update__content")
                print("{} total updates collected till now".format(len(update_cards)))

            if element_exists(driver, "section.product-index__timeline"):
                product_update_content = driver.find_element_by_css_selector("section.product-index__timeline")
                update_cards = product_update_content.find_elements_by_css_selector("div.product-update__content")
            print("Total updates for this product : {}".format(len(update_cards)))
        except Exception as e:
            print("Exception when collecting update links : " + str(e))
            print("Try count is {}".format(loop_count))
        loop_count += 1

    return update_cards


def get_product_data(start, end):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=YouKnowWho")
    driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
    driver.maximize_window()
    count = 0

    product_links = get_product_links()
    try:
        for i in range(start, end):
            product_url = product_links[i]
            try:
                print("Collecting data for product: {}".format(product_url))
                driver.get(product_url)
                sleep_randomly()

                product = dict()
                product['url'] = product_url
                try:
                    product_header_content = driver.find_element_by_css_selector("div.product-header__content")
                    title = product_header_content.find_element_by_css_selector("h1.product-header__title").text
                    product['title'] = title.strip()
                    tagline = product_header_content.find_element_by_css_selector("p.product-header__tagline").text
                    product['tagline'] = tagline.strip()
                    tags = product_header_content.find_elements_by_css_selector("div.tag-list__tag")
                    taglist = []
                    for tag in tags:
                        taglist.append(tag.text.strip())
                    product['tags'] = taglist
                except Exception as e:
                    print("Exception when collecting taglines, titles and tags: " + str(e))

                try:
                    product_metrics_content = driver.find_element_by_css_selector("div.product-metrics__content")
                    updates = product_metrics_content.find_element_by_css_selector("a.product-metrics__stat.product-metrics__stat--updates.active.ember-view")
                    product["num_updates"] = updates.text.strip()
                except Exception as e:
                    print("Exception when collecting num of updates: " + str(e))

                try:
                    followers = product_metrics_content.find_element_by_css_selector(
                        "a.product-metrics__stat.product-metrics__stat--followers.ember-view")
                    product["num_followers"] = followers.text.strip()
                except Exception as e:
                    print("Exception when collecting followers: " + str(e))

                try:
                    revenue = product_metrics_content.find_element_by_css_selector(
                        "a.product-metrics__stat.product-metrics__stat--revenue.ember-view")
                    product["revenue"] = revenue.text.replace("\n", ",").strip()
                except Exception as e:
                    print("Exception when collecting revenue: " + str(e))

                try:
                    product_content = driver.find_element_by_css_selector("div.product__content")
                    description =\
                        product_content.find_element_by_css_selector("section.product-sidebar__description").text
                    product["description"] = description
                except Exception as e:
                    print("Exception when collecting description: " + str(e))

                try:
                    users = product_content.find_elements_by_css_selector\
                        ("div.user-link.product-sidebar__user-link.ember-view")
                    user_list = []
                    for user in users:
                        user_list.append(user.text)
                    product["founders"] = user_list
                except Exception as e:
                    print("Exception when collecting founders: " + str(e))

                sleep_randomly()
                try:
                    # update_cards = []
                    # product_update_links = []
                    # if element_exists(driver, "section.product-index__timeline"):
                    #     product_update_content = driver.find_element_by_css_selector("section.product-index__timeline")
                    #     update_cards = product_update_content.find_elements_by_css_selector("div.product-update__content")
                    # while element_exists(driver, "button.product-index__load-more-button.load-more-button.ember-view"):
                    #     load_more_button = driver.find_element_by_class_name(
                    #             "product-index__load-more-button.load-more-button.ember-view")
                    #     load_more_button.click()
                    #     count = 20
                    #     while count:
                    #         driver.execute_script('window.scrollTo(0, 50*document.body.scrollHeight);')
                    #         count -= 1
                    #     sleep_randomly()
                    #
                    #     product_index_timeline = driver.find_element_by_css_selector("section.product-index__timeline")
                    #     update_cards = product_index_timeline.find_elements_by_css_selector("div.product-update__content")
                    #     print("{} total updates collected till now".format(len(update_cards)))
                    #
                    # if element_exists(driver, "section.product-index__timeline"):
                    #     product_update_content = driver.find_element_by_css_selector("section.product-index__timeline")
                    #     update_cards = product_update_content.find_elements_by_css_selector("div.product-update__content")
                    # print("Total updates for this product : {}".format(len(update_cards)))

                    product_update_links = []
                    update_cards = get_updates(driver, product_url)
                    for card in update_cards:
                        update_link = card.find_element_by_css_selector("a.product-update__title.ember-view")
                        product_update_links.append(update_link.get_attribute("href"))
                    product["update_links"] = product_update_links
                except Exception as e:
                    print("Exception when collecting update links: " + str(e))


                try:
                    print("Collecting Followers...")
                    followers = get_followers(driver, product_url)
                    product["followers"] = followers
                except Exception as e:
                    print("Exception when collecting followers: " + str(e))

                sleep_randomly()
                count += 1
                print("Total products collected : {}".format(count))
                with open("product_" + str(i) + '.pickle', 'wb') as handle:
                    pickle.dump(product, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("----------------------------------------------------------")
            except Exception as e:
                print("Exception happened: " + str(e))
                break
    finally:
        driver.quit()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("You need two arguments to run this script. start and end for product links file")
    else:
        start, end = int(sys.argv[1]), int(sys.argv[2])
        get_product_data(start, end)

