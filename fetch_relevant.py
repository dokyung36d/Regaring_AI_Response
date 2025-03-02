from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
import os
import certifi
from key import openai_key
# from key import mongodb_password

ca = certifi.where()

embedding_model = OpenAIEmbeddings(api_key=openai_key)

mongodb_password = os.getenv("mongodb_password")

uri = f"mongodb+srv://dokyung36d:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile = ca)

def fetch_relevant_document(query_text, database, collection, num_fetched, index_name):
    vector_store = MongoDBAtlasVectorSearch(
    collection=client[database][collection],
    embedding=embedding_model,
    text_key="page_content",
    index_name=index_name,
    embedding_key="hobby_embedding",
    relevance_score_fn="cosine")

    similar_docs = vector_store.similarity_search(query_text, k=num_fetched)

    # 결과에서 필요한 필드 추출 (예: 문서 전체 내용 혹은 특정 메타데이터 등)
    # 필요한 key가 있다면 아래를 수정
    retrieved_hobby_list = [doc.page_content for doc in similar_docs]

    return retrieved_hobby_list