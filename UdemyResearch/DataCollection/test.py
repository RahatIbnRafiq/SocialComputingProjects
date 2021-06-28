from pyudemy import Udemy
import pymongo

CLIENT_ID = "gBvBsv3yfCyBVcqs2BzkWewyRHwhQceIE3Q51cL0"
CLIENT_SECRET = "L5lDPQuomOwd7AZTpWatfwouHOnhDduDS46RPKQbvleL50Q2xFldgLJ1A8Drs7hMqHWmKusH7s2Wdg5X46ReoGBNdBCt2gCMVC7eGdiWvEgGp06IU9N4cU7YfHuFFPlB"


def test1():
    udemy = Udemy(CLIENT_ID, CLIENT_SECRET)
    courses = udemy.courses(page=1, page_size=100)
    courses = courses['results']
    print(len(courses))


def test2():
    udemy = Udemy(CLIENT_ID, CLIENT_SECRET)
    courses = udemy.courses(page=1, page_size=100)
    courses = courses['results']
    print(len(courses))


def mongo_test():
    client = pymongo.MongoClient()
    mydb = client["mydb"]
    mycol = mydb["people"]
    data = {'name': 'rahat', 'age' : 33}
    mycol.insert_one(data)


mongo_test()


