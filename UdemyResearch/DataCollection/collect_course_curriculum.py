import pymongo
from pyudemy import Udemy

import constants
import utils


def get_course_ids_from_db():
    course_col = utils.get_mongo_collection(client, "udemy", "courses")
    curriculum_col = utils.get_mongo_collection(client, "udemy", "curriculum")
    cursor = course_col.find({})
    course_ids = set()
    for document in cursor:
        course_ids.add(document["id"])
    print("Total courses: " + str(len(course_ids)))

    for course_id in course_ids:
        course = {}
        page_count = 1
        while True:
            curriculum = udemy.public_curriculum(course_id, page=page_count, page_size=100)
            print("__________________________________________________________")
            print("Course curriculum size for " + str(course_id) + " is : " + str(curriculum["count"]))
            course["id"] = course_id
            course["curriculum"] = curriculum["results"]
            if curriculum['next'] is None:
                print("Done collecting curriculum!!!")
                break
            page_count += 1
            print("Page count is now: " + str(page_count))
            utils.sleep_randomly()
        print("Curriculum size for this is course is : " + str(len(course["curriculum"])))
        curriculum_col.insert_one(course)
        print("Total number of courses inserted till now: " + str(curriculum_col.count_documents({})))
        print("__________________________________________________________")


udemy = Udemy(constants.UDEMY_CLIENT_ID, constants.UDEMY_CLIENT_SECRET)
client = pymongo.MongoClient()
get_course_ids_from_db()
client.close()
