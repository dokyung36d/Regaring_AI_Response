import json
import os
from openai import OpenAI
import csv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

openai_key = os.getenv("openai_key")
mongodb_password = os.getenv("mongodb_password")
mongodb_username = os.getenv("mongodb_username")

uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
mongodb_client = MongoClient(uri, server_api=ServerApi('1'))

database = mongodb_client["newspaperTitle"]
collection = database["title"]


openai_org_id = os.getenv("openai_org_id")

openai_client = OpenAI(
  organization=openai_org_id,
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
