import pymongo


def get_mongo_collection(client, db_name, col_name):
    db = client[db_name]
    col = db[col_name]
    return col


def get_post_links_from_db():
    client = pymongo.MongoClient()
    group_collection = get_mongo_collection(client, "indie_hackers", "groups")
    groups = group_collection.find({})
    all_posts = []
    for group in groups:
        print(len(group["data"]["posts"]))
        for post in group["data"]["posts"]:
            all_posts.append(post)
    client.close()
    f = open("post_links.txt", "w")
    for post in all_posts:
        f.write(post+"\n")
    f.close()


get_post_links_from_db()


