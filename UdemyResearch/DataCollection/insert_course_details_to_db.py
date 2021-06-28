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


def clean_up_data(course):
    d = dict()

    if 'rating' in course:
        rating = course['rating']
        items = rating.split("\n")
        d['rating'] = float(items[1])
        index1 = items[2].index("(") + len("(")
        index2 = items[2].index("rating")
        d['num_ratings'] = float(items[2][index1:index2].strip().replace(",",""))

    if 'num_students' in course:
        try:
            num_students = course['num_students']
            index1 = num_students.index("students")
            num_students = num_students[:index1].strip()
            d['num_students'] = float(num_students.strip().replace(",",""))
        except Exception:
            pass

    if 'locale' in course:
        d['locale'] = course['locale']

    if 'sidebar_info' in course:
        sidebar_info = course['sidebar_info']
        items = sidebar_info.split("\n")
        for item in items:
            item = item.strip()
            if "downloadable resource" in item:
                index1 = item.index("downloadable resource")
                d["num_downloadable_resources"] = int(item[:index1].strip())
            elif "on-demand video" in item:
                if "hour" in item:
                    index1 = item.index("hour")
                    d["on_demand_video_minutes"] = float(item[:index1].strip()) * 60.0
                elif "min" in item:
                    index1 = item.index("min")
                    d["on_demand_video_minutes"] = float(item[:index1].strip())
            elif "Full lifetime access" in item:
                d["full_lifetime_access"] = True
            elif "Access on" in item:
                if "mobile" in item:
                    d["mobile_access"] = True
                if "TV" in item:
                    d["tv_access"] = True
            elif "Certificate of completion" in item:
                d['certificate_of_completion'] = True
            elif "article" in item:
                index1 = item.index("article")
                d["num_articles"] = float(item[:index1].strip().replace(",", ""))

    if 'captions' in course:
        captions = course['captions'].replace("\"","").replace("[Auto]","")
        index1 = captions.index("[") + len("[")
        index2 = captions.index("}")
        captions = captions[index1:index2]
        items = captions.split(",")
        items = [item.replace("]", "").strip() for item in items]
        d['captions'] = items

    if 'instructor_info' in course:
        instructor_infos = course['instructor_info']
        obj = json.loads(instructor_infos)
        for key in obj.keys():
            if "course_id" in key:
                d["course_id"] = obj['course_id']
            elif "instructors_info" in key:
                for item in obj[key]:
                    for sec_key in item.keys():
                        d["instructors_info_"+sec_key] = item[sec_key]

    return d


def insert_to_db():
    location = "/Users/rahatibnrafiq/Downloads/udemy_course_details/"
    filenames = get_all_files(location)
    course_details_collection = get_mongo_collection("udemy", "course_details")
    for filename in filenames:
        if "pickle" not in filename:
            continue
        with open(location+filename, 'rb') as handle:
            try:
                b = pickle.load(handle)
                course = clean_up_data(b)
                course_details_collection.insert_one(course)
            except Exception as e:
                print("Exception happened: ", filename, e, b)
                break


insert_to_db()
client.close()
