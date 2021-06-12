from selenium import webdriver
import constants
import utils
import pymongo


def get_mongo_collection(db_name, col_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    col = db[col_name]
    return col


def get_interview_links():
    links = set()
    f = open("interview_links.txt", "r")
    for line in f:
        links.add(line.strip())
    f.close()
    print(len(links))
    return links


def get_interview_data():
    options = webdriver.ChromeOptions()
    options.headless = True
    links = get_interview_links()
    driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH, options=options)
    interviews = []
    try:
        for link in links:
            print("--------------------------------------------------------------")
            print("Collecting data for link: " + link)
            interview = {}
            driver.get(link)
            utils.sleep_randomly()
            try:
                interviewee_name = driver.find_element_by_class_name("user-link__name")
                intervieweee_username = driver.find_element_by_css_selector("a.user-link__link.ember-view")
                interview["interviewee_name"] = interviewee_name.text
                interview["interviewee_username"] = intervieweee_username.get_attribute("href")
            except Exception as e:
                print("Exception when getting interviewee name: " + str(e))

            try:
                title = driver.find_element_by_class_name("interview-header__title")
                interview["title"] = title.text
            except Exception as e:
                print("Exception when getting interview title: " + str(e))

            try:
                updates =\
                    driver.find_element_by_css_selector("a.product-metrics__stat.product-metrics__stat--updates.ember-view")
                interview["updates"] = updates.text.strip()
            except Exception as e:
                print("Exception when getting interview updates: " + str(e))

            try:
                revenue = \
                    driver.find_element_by_css_selector("a.product-metrics__stat.product-metrics__stat--revenue.ember-view")
                interview["revenue"] = revenue.text.strip()
            except Exception as e:
                print("Exception when getting interview revenue: " + str(e))

            try:
                total_votes = driver.find_element_by_class_name("thread-voter__count")
                interview["total_votes"] = total_votes.text.strip()
            except Exception as e:
                print("Exception when getting interview total votes: " + str(e))

            try:
                interview_body = driver.find_element_by_css_selector("div.interview-body.ember-view")
                interview["interview_body"] = interview_body.text.strip()
            except Exception as e:
                print("Exception when getting interview body: " + str(e))

            try:
                all_comments = driver.find_element_by_class_name("interview-comments")
                comments = all_comments.find_elements_by_css_selector("div.comment.comment--on-desktop.ember-view")
                comment_list = []
                for comment in comments:
                    comment_dict = {}

                    comment_voter_score = comment.find_element_by_class_name("comment-voter__score")
                    comment_dict["comment_voter_score"] = comment_voter_score.text

                    commenter_username = comment.\
                        find_element_by_css_selector("span.user-link__name.user-link__name--username")
                    comment_dict["commenter_username"] = commenter_username.text

                    comment_timestamp = comment.find_element_by_class_name("footer__date")
                    comment_dict["comment_timestamp"] = comment_timestamp.get_attribute("title")
                    comment_dict["comment_time_ago"] = comment_timestamp.text
                    comment_list.append(comment_dict)
            except Exception as e:
                print("Exception when getting interview comments: " + str(e))

            print("total comments collected: " + str(len(comments)))
            interview["comments"] = comment_list
            interviews.append(interview)
            utils.sleep_randomly()
            print("Total interviews collected so far: " + str(len(interviews)))
            print("--------------------------------------------------------------")
    except Exception as e:
        print("Exception happened: " + str(e))
    finally:
        driver.quit()
    print("Total interviews collected: " + str(len(interviews)))
    return interviews


def collect_and_insert_interviews():
    interviews_collection = get_mongo_collection("indie_hackers", "interviews")
    interviews = get_interview_data()
    for interview in interviews:
        interviews_collection.insert_one(interview)


collect_and_insert_interviews()
