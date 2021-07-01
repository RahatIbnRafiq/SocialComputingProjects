from selenium import webdriver
import constants
import time
import random
import sys
import pickle


def sleep_randomly():
    random_sleep = random.randint(5, 10)
    time.sleep(random_sleep)


def get_all_post_links():
    post_links = []
    f = open("product_posts.txt", "r")
    for line in f:
        post_links.append(line.strip())
    f.close()
    return post_links


def get_posts(start, end):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920,1080")
    post_links = get_all_post_links()
    count = -1
    for i in range(start, end):
        post = dict()
        post_link = post_links[i]
        print("-------------------------------------------------------")
        print("Value of i is: "+str(i))
        print("Collecting data for post: " + str(post_link))
        driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
        try:
            driver.maximize_window()
            driver.get(post_link)
            sleep_randomly()
            post['post_link'] = post_link
            post_page_element = None

            try:
                post_page_element = driver.find_element_by_css_selector("div.post-page__content")
                title = post_page_element.find_element_by_css_selector("h1.post-page__title")
                post['title'] = title.text
            except Exception:
                post['title'] = ""

            if post_page_element is None:
                continue

            try:
                poster_link = post_page_element.find_element_by_css_selector("a.ember-view.post-page__byline")
                poster_link = poster_link.get_attribute('href')
                post['poster_link'] = poster_link
            except Exception:
                post['poster_link'] = ""

            try:
                post_liker_count = post_page_element.find_element_by_css_selector("div.post-liker__count").text
                post['post_liker_count'] = post_liker_count
            except Exception:
                post['post_liker_count'] = 0


            try:
                post_body = post_page_element.find_element_by_css_selector("div.post-page__body.content.ember-view")
                post['post_body'] = post_body.text
            except Exception:
                post['post_body'] = ""


            try:
                attached_link = post_page_element.find_element_by_css_selector("a.attached-link__link").get_attribute("href")
                attached_link_text = post_page_element.find_element_by_css_selector("div.attached-link__text").text
                post['attached_link'] = attached_link
                post['attached_link_text'] = attached_link_text.strip()
            except Exception:
                post['attached_link'] = ""
                post['attached_link_text'] = ""

            all_comments = []
            post_page_comments = post_page_element.find_elements_by_css_selector("div.comment.comment--on-desktop.ember-view")
            for comment in post_page_comments:
                try:
                    comment_dict = dict()
                    comment_voter_score = comment.find_element_by_css_selector("div.comment-voter__score").text
                    commenter = comment.find_element_by_css_selector("div.user-link.footer__user-link.ember-view").text
                    comment_date = comment.find_element_by_css_selector("a.footer__date.ember-view").get_attribute("title")
                    comment_text = comment.find_element_by_css_selector("div.comment__content.content.ember-view").text

                    comment_dict['voter_score'] = comment_voter_score
                    comment_dict['commenter'] = commenter
                    comment_dict['comment_date'] = comment_date
                    comment_dict['comment_text'] = comment_text.strip()
                    all_comments.append(comment_dict)
                except Exception:
                    continue
            post['post_comments'] = all_comments

            with open("post_"+str(i)+'.pickle', 'wb') as handle:
                pickle.dump(post, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Collecting and writing data for post: " + str(post_link)+" is done.")
            count += 1
            print("Total posts collected till now: " + str(count))
            print("-----------------------------------------------------")
        finally:
            driver.quit()


def read_posts():
    for i in range(0, 5):
        with open('post_'+str(i)+'.pickle', 'rb') as handle:
            b = pickle.load(handle)
            print(b)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("You need two arguments to run this script. start and end index for the product_posts file")
    else:
        start, end = int(sys.argv[1]), int(sys.argv[2])
        get_posts(start, end)
