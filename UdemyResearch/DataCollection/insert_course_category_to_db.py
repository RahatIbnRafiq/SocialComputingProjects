from os import listdir
from os.path import isfile, join
import pymongo
import pickle
import json

client = pymongo.MongoClient()


def get_mongo_collection(db_name, col_name):

    db = client[db_name]
    col = db[col_name]
    return col


def get_all_files(location):
    files = [f for f in listdir(location) if isfile(join(location, f))]
    return files


def insert_to_db():
    location = "/Users/rahatibnrafiq/Research/course_categories/"
    filenames = get_all_files(location)
    course_categories_collection = get_mongo_collection("udemy", "course_categories")
    for filename in filenames:
        if "pickle" not in filename:
            continue
        with open(location+filename, 'rb') as handle:
            try:
                course = pickle.load(handle)
                # course = clean_up_data(b)
                course_categories_collection.insert_one(course)
            except Exception as e:
                print("Exception happened: ", filename, e, course)
                break


insert_to_db()
client.close()
