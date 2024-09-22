from key import openai_key

from openai import OpenAI
import csv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from key import mongodb_password

uri = f"mongodb+srv://dokyung36d:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
mongodb_client = MongoClient(uri, server_api=ServerApi('1'))

database = mongodb_client["RAG"]
collection = database["embedding"]


openai_client = OpenAI(
  organization='org-RSWEbMw552t3xBqgzkF6w547',
  api_key=openai_key
)

# File path to your CSV file
file_path = 'hobbies_and_names.csv'

# Open the CSV file using 'with open'
with open(file_path, mode='r', encoding='utf-8') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    # Read each row
    for row in reader:
        # Example of accessing specific columns:
        hobby, name = row[0], row[1]  # First column (취미)
        print(hobby, name)

        responese = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=hobby,
            encoding_format="float"
            )

        embedding_vector = responese.data[0].embedding

        dict = {
            "name" : name,
            "hobby" : hobby,
            "hobby_embedding" : embedding_vector
        }

        collection.insert_one(dict)
