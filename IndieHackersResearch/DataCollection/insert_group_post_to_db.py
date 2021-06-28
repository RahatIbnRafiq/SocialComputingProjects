from os import listdir
from os.path import isfile, join
import json
import re

import pymongo


def get_mongo_collection(db_name, col_name):
    client = pymongo.MongoClient()
    db = client[db_name]
    col = db[col_name]
    return col

def get_all_files(location):
    files = [f for f in listdir(location) if isfile(join(location, f))]
    return files


def insert_posts_to_db():
    location = "/Users/rahatibnrafiq/MyWorkSpace/SocialComputingProjects/IndieHackersResearch/DataCollection/group_posts/"
    files = get_all_files(location)
    for file in files:
        write_group_about(location+file)
        write_group_member_no(location+file)
        write_group_moderators(location + file)
        write_group_posts(location + file)
    insert_to_db()


def write_group_posts(file):
    f = open(file, "r")
    for line in f:
        line = line.strip()
        group = dict()

        index1 = line.index("\'group\': ") + len("\'group\': ")
        index2 = line.index("\'posts\': ")
        group_text = line[index1:index2]
        group_text = group_text.replace("'", "").replace(",", "")

        index1 = line.index("\'posts\': ") + len("\'posts\': ")
        index2 = line.index("\'about\': ")
        posts_text = line[index1:index2]
        posts = posts_text.split(",")
        post_links = []
        for post in posts:
            post = post.replace("'", "").replace("]", "").replace("[", "").strip()
            if len(post) > 3:
                post_links.append(post)
        group["group_url"] = group_text
        group["posts"] = post_links
        json_object = json.dumps(group)
        g = open("group_posts.txt", "a")
        g.write(json_object+"\n")
        g.close()
    f.close()


def write_group_moderators(file):
    f = open(file, "r")
    for line in f:
        line = line.strip()
        line = line.strip()
        group = dict()

        index1 = line.index("\'group\': ") + len("\'group\': ")
        index2 = line.index("\'posts\': ")
        group_text = line[index1:index2]
        group_text = group_text.replace("'", "").replace(",", "")

        index1 = line.index("\'about\': ") + len("\'about\': ")
        about = line[index1:]
        about = about.replace("[", "")
        about = about.replace("]", "")
        about = about.replace("{", "")
        about = about.replace("}", "")
        about = about.replace("'", "")

        to_write = "\n"

        if "moderated by" in about:
            index1 = about.index("moderated by,") + len("moderated by,")
            moderated_by = about[index1:]
            moderators = moderated_by.split(",")
            to_write = group_text + "," + str(len(moderators)) + "," + ':'.join(moderators) + "\n"
        else:
            to_write = group_text + "," + str(0) + "," + "\n"
        g = open("group_moderators.txt", "a")
        g.write(to_write)
        g.close()
    f.close()


def write_group_member_no(file):
    f = open(file, "r")
    for line in f:
        line = line.strip()
        line = line.strip()

        index1 = line.index("\'group\': ") + len("\'group\': ")
        index2 = line.index("\'posts\': ")
        group_text = line[index1:index2]
        group_text = group_text.replace("'", "").replace(",", "")

        index1 = line.index("\'about\': ") + len("\'about\': ")
        about = line[index1:]
        about = about.replace("[", "")
        about = about.replace("]", "")
        about = about.replace("{", "")
        about = about.replace("}", "")
        about = about.replace("'", "")
        members = 0
        if "member" in about:
            index1 = about.index("member")
            members = ""
            if index1 < 10:
                members = about[: index1]
            else:
                members = about[index1 - 10:index1]
            members = re.sub('\D', '', members)
        g = open("group_members.txt", "a")
        g.write(str(group_text) + "," + str(members) + "\n")
        g.close()
    f.close()


def write_group_about(file):
    f = open(file, "r")
    for line in f:
        line = line.strip()
        line = line.strip()

        index1 = line.index("\'group\': ") + len("\'group\': ")
        index2 = line.index("\'posts\': ")
        group_text = line[index1:index2]
        group_text = group_text.replace("'", "").replace(",", "")

        index1 = line.index("\'about\': ") + len("\'about\': ")
        about = line[index1:]
        index1 = about.index("member")
        about = about[: index1]
        final_about = re.sub(r'[^a-zA-Z ]+', ' ', about)
        g = open("group_abouts.txt", "a")
        g.write(str(group_text) + "," + str(final_about) + "\n")
        g.close()
    f.close()



def insert_to_db():
    group_dict = dict()

    f = open("group_moderators.txt", "r")
    for line in f:
        d = {}
        line = line.strip()
        items = line.split(",")
        group_url = items[0].strip()
        num_moderators = items[1]
        moderators = items[2].split(":")
        d["num_moderators"] = num_moderators
        d["moderators"] = moderators
        group_dict[group_url] = d
    f.close()

    f = open("group_members.txt", "r")
    for line in f:
        line = line.strip()
        items = line.split(",")
        group_dict[items[0].strip()]["members"] = items[1]
    f.close()

    f = open("group_abouts.txt", "r")
    for line in f:
        line = line.strip()
        items = line.split(",")
        group_dict[items[0].strip()]["about_text"] = items[1]
    f.close()

    f = open("group_posts.txt", "r")
    for line in f:
        line = line.strip()
        json_obj = json.loads(line)
        group_posts = json_obj['posts']
        group_url = json_obj['group_url'].strip()
        group_dict[group_url]["posts"] = group_posts
    f.close()

    group_collection = get_mongo_collection("indie_hackers", "groups")
    for key in group_dict.keys():
        d = dict()
        d["group"] = key
        d["data"] = group_dict[key]
        group_collection.insert_one(d)


insert_posts_to_db()
