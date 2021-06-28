import pymongo
from pyudemy import Udemy
import sys

import constants
import utils


def get_course_ids_from_db(start, udemy, client):
    course_col = utils.get_mongo_collection(client, "udemy", "final_courses")
    reviews_col = utils.get_mongo_collection(client, "udemy", "reviews")
    cursor = course_col.find({})
    course_ids = set()
    for document in cursor:
        course_ids.add(document["id"])
    print("Total courses: " + str(len(course_ids)))
    course_ids = list(course_ids)
    course_ids = sorted(course_ids)

    for i in range(start, len(course_ids)):
        print("__________________________________________________________")
        print("Value of i is: " + str(i))
        course_id = course_ids[i]
        course = {}
        page_count = 1
        course["id"] = course_id
        course["review"] = []
        while True:
            utils.sleep_randomly()
            review = udemy.course_reviews(course_id, page=page_count, page_size=100)
            print("Course review size for " + str(course_id) + " is : " + str(review["count"]))
            course["id"] = course_id
            course["review"] += review["results"]
            if review['next'] is None:
                print("Done collecting review!!!")
                break
            page_count += 1
            print("Page count is now: " + str(page_count))
        print("Review collected for this is course is : " + str(len(course["review"])))
        reviews_col.insert_one(course)
        print("Total number of courses inserted till now: " + str(reviews_col.count_documents({})))
        print("__________________________________________________________")


def start_collecting(start):
    try:
        udemy = Udemy(constants.UDEMY_CLIENT_ID, constants.UDEMY_CLIENT_SECRET)
        client = pymongo.MongoClient()
        get_course_ids_from_db(start, udemy, client)
        client.close()
    except Exception as e:
        print(e)
    finally:
        client.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You need one argument to run this script. start index for the course link list")
    else:
        start = int(sys.argv[1])
        start_collecting(start)
