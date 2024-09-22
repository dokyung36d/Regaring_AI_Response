from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from key import mongodb_password
from key import openai_key
from openai import OpenAI

string = "Turkish Food is Delicious!!"

uri = f"mongodb+srv://dokyung36d:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
mongodb_client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

test_database = mongodb_client["test"]
test_collection = test_database["test"]


openai_client = OpenAI(
  organization='org-RSWEbMw552t3xBqgzkF6w547',
  api_key=openai_key
)


responese = openai_client.embeddings.create(
  model="text-embedding-ada-002",
  input=string,
  encoding_format="float"
)

embedding_vector = responese.data[0].embedding

dict = {
    "key" : string,
    "embedding" : embedding_vector
}

test_collection.insert_one(dict)