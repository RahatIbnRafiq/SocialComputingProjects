from os import listdir
from os.path import isfile, join
import pickle
import pymongo

client = pymongo.MongoClient()


def get_mongo_collection(db_name, col_name):
    db = client[db_name]
    col = db[col_name]
    return col


def get_all_files(location):
    files = [f for f in listdir(location) if isfile(join(location, f))]
    return files


def insert_product_posts_to_db():
    location = "/Users/rahatibnrafiq/Downloads/product_data/"
    files = get_all_files(location)
    products_collection = get_mongo_collection("indie_hackers", "products")
    for filename in files:
        if ".pickle" not in filename:
            continue
        with open(location + filename, 'rb') as handle:
            post = pickle.load(handle)
            products_collection.insert_one(post)


def get_all_product_posts_to_file():
    products_collection = get_mongo_collection("indie_hackers", "products")
    products = products_collection.find({})
    all_update_links = []
    for product in products:
        if "update_links" in product:
            all_update_links += product["update_links"]

    all_update_links = list(set(all_update_links))
    print(len(all_update_links))
    with open("product_posts.txt", "w") as f:
        for update_link in all_update_links:
            f.write(update_link.strip() + "\n")


get_all_product_posts_to_file()
client.close()
