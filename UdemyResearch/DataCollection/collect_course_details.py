import pymongo
from pyudemy import Udemy

import constants
import mongo_utils


def get_course_ids_from_db():
    course_col = mongo_utils.get_mongo_collection(client, "udemy", "courses")
    cursor = course_col.find({})
    course_ids = set()
    for document in cursor:
        course_ids.add(document["id"])
    print("Total courses: " + str(len(course_ids)))

    for course_id in course_ids:
        course_detail = udemy.course_detail(course_id)
        print(course_detail)
        break


udemy = Udemy(constants.UDEMY_CLIENT_ID, constants.UDEMY_CLIENT_SECRET)
client = pymongo.MongoClient()
get_course_ids_from_db()
client.close()
