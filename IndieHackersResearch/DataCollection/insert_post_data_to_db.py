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
    location = "/Users/rahatibnrafiq/Downloads/product_post_details/"
    files = get_all_files(location)
    posts_collection = get_mongo_collection("indie_hackers", "product_posts")
    for filename in files:
        if ".pickle" not in filename:
            continue
        print(filename)
        with open(location+filename, 'rb') as handle:
            post = pickle.load(handle)
            posts_collection.insert_one(post)
        print(len(files))


insert_posts_to_db()
client.close()


