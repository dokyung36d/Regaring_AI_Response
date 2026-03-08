from pymongo import MongoClient
import os
mongodb_password = os.getenv("mongodb_password")

def ConnectMongoDB():
    client = MongoClient("mongodb://localhost:27017")
    mydb = client["signup"]
    mycol = mydb["userinfo"]
    return mycol

def insert_one(coll):
    mydict = {
        "name" : "Byeong-Chang-Min",
        "age" : 35,
        "address" : "수원시",
        "phone" : "010-1234-4321"
    }
    coll.insert_one(mydict)

def select_one(coll):
    result = coll.find_one()
    print(result)

def select_all(coll):
    result = list(coll.find())
    for i in result:
        print(i)

if __name__ == '__main__':
    coll = ConnectMongoDB()
    insert_one(coll)
    print("findOne 쿼리")
    select_one(coll)
    print("findAll 쿼리")
    select_all(coll)