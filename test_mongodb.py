from pymongo import MongoClient
from key import mongodb_password

# def ConnectMongoDB():
#     client = MongoClient("mongodb://localhost:27017");
#     mydb = client["signup"]
#     mycol = mydb["userinfo"]
#     return mycol

# def insert_one(coll):
#     mydict = {
#         "name" : "Byeong-Chang-Min",
#         "age" : 35,
#         "address" : "수원시",
#         "phone" : "010-1234-4321"
#     }
#     coll.insert_one(mydict)

# if __name__ == '__main__':
#     coll = ConnectMongoDB()
#     insert_one(coll)

# def ConnectMongoDB():
#     client = MongoClient("mongodb://localhost:27017")
#     mydb = client["signup"]
#     mycol = mydb["userinfo"]
#     return mycol

# def select_one(coll):
#     result = coll.find_one()
#     print(result)

# def select_all(coll):
#     result = list(coll.find())
#     for i in result:
#         print(i)

# if __name__ == '__main__':
#     coll = ConnectMongoDB()
#     print("findOne 쿼리")
#     select_one(coll)
#     print("findAll 쿼리")
#     select_all(coll)

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = f"mongodb+srv://dokyung36d:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)