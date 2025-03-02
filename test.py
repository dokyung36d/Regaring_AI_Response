from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
import os
from key import openai_key
# from key import mongodb_password

# ca = certifi.where()
# mongodb_password = os.getenv("mongodb_password")

# uri = f"mongodb+srv://dokyung36d:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile = ca)
# # MongoDB 클라이언트 설정

# # OpenAI Embedding 설정
# embeddings = OpenAIEmbeddings(openai_api_key = openai_key)

# database="RAG"
# collection="embedding"
# key="hobby"
# num_fetched=1

# # VectorStore 초기화
# vector_store = MongoDBAtlasVectorSearch(
#     collection=client[database][collection],
#     embedding=embeddings
# )

# query = "How can I use vector search in MongoDB?"

# # 유사 문서 검색
# similar_docs = vector_store.similarity_search(query, k=3)

# print("hello world")
# # 결과 출력
# for i, doc in enumerate(similar_docs, 1):
#     print(f"Result {i}: {doc.page_content}")
#     print("heello world")

from generate_random_hobby_and_newspaper_title import generate_hobby_and_newspaper_tile
from embedding import get_embedding
from fetch_relevant import fetch_relevant_document
from prompt import get_relevant_newspapers, get_recommend_advertise
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import redis
import json


generated_newspaper_title_embedding = get_embedding("mlb word")

retreived_hobby = fetch_relevant_document(generated_newspaper_title_embedding, database="RAG", collection="embedding", key="hobby", num_fetched=1, index_name="hobby_vector_index")
print("hellow rodl")