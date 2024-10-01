import json
from key import openai_key

from openai import OpenAI
import csv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from key import mongodb_password

uri = f"mongodb+srv://dokyung36d:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
mongodb_client = MongoClient(uri, server_api=ServerApi('1'))

database = mongodb_client["newspaperTitle"]
collection = database["title"]


openai_client = OpenAI(
  organization='org-RSWEbMw552t3xBqgzkF6w547',
  api_key=openai_key
)


# Load the JSON file
with open('VL_span_extraction.json', 'r', encoding='utf-8') as file:
    data = json.load(file)



for i in range(len(data["data"])):
    newspaper_title = data["data"][i]["doc_title"]

    responese = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=newspaper_title,
            encoding_format="float"
            )

    embedding_vector = responese.data[0].embedding

    dict = {
        "newspaper_title" : newspaper_title,
        "hobby_embedding" : embedding_vector
    }

    collection.insert_one(dict)

    if i % 50 == 0:
        print(newspaper_title)
