from os import listdir
from os.path import isfile, join
import pymongo
import pickle


client = pymongo.MongoClient()


def get_mongo_collection(db_name, col_name):
    db = client[db_name]
    col = db[col_name]
    return col


def get_all_files(location):
    files = [f for f in listdir(location) if isfile(join(location, f))]
    return files


def insert_posts_to_db():
    location = "/Users/rahatibnrafiq/Downloads/indiehacker_posts/"
    files = get_all_files(location)
    posts_collection = get_mongo_collection("indie_hackers", "posts")
    for filename in files:
        if ".pickle" not in filename:
            continue
        with open(location+filename, 'rb') as handle:
            post = pickle.load(handle)
            posts_collection.insert_one(post)


insert_posts_to_db()
client.close()


