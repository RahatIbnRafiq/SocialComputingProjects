from pyudemy import Udemy
import pymongo
import time

import constants


def get_mongo_collection(db_name, col_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    col = db[col_name]
    return col


def get_subcategories():
    subcategories = []
    f = open("subcategories.txt", "r")
    for line in f:
        subcategories.append(line.strip())
    f.close()
    return subcategories


def get_insert_courses(subcategory, courses_col):
    udemy = Udemy(constants.UDEMY_CLIENT_ID, constants.UDEMY_CLIENT_SECRET)
    courses = udemy.courses(page=1, page_size=10, subcategory=subcategory)
    courses_count = courses["count"]
    courses = courses['results']
    print("Total courses for this subcategory : " + str(courses_count))
    all_courses = courses
    page_count = 2

    while len(all_courses) < courses_count:
        courses = udemy.courses(page=page_count, page_size=100, subcategory=subcategory)
        courses = courses['results']
        all_courses += courses
        page_count += 1
        print("Courses collected till now for this subcategory: " + str(len(all_courses)))
        time.sleep(15)
    print("final number of courses collected: " + str(len(all_courses)))

    for course in all_courses:
        try:
            courses_col.insert_one(course)
        except Exception:
            continue
    print("Total number of courses collected till now: " + str(courses_col.count_documents({})))


def get_courses_by_subcategories():
    courses_col = get_mongo_collection("udemy", "courses")
    subcategories = get_subcategories()
    for subcategory in subcategories[:1]:
        print("---------------------------------------------------------------")
        print("Collecting courses for subcategory: " + subcategory)
        get_insert_courses(subcategory, courses_col)
        print("Done for subcategory: " + subcategory)
        print("---------------------------------------------------------------")


get_courses_by_subcategories()

