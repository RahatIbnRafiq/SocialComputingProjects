from pyudemy import Udemy
import pymongo
import time

import constants

client = client = pymongo.MongoClient()


def get_mongo_collection(db_name, col_name):
    db = client[db_name]
    col = db[col_name]
    return col

# 1928374
# 1931790
# 2199310
# 2312768
# 2510530


def remove_duplicate_courses():
    course_ids = set()
    course_collection = get_mongo_collection("udemy", "courses")
    final_course_collection = get_mongo_collection("udemy", "final_courses")
    courses = course_collection.find()
    for course in courses:
        course_ids.add(course["id"])
    print(len(course_ids))

    for course_id in course_ids:
        course = course_collection.find_one({"id": course_id})
        final_course_collection.insert_one(course)


remove_duplicate_courses()
client.close()
