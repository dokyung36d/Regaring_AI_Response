from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
import os
import certifi
from key import openai_key

ca = certifi.where()

mongodb_password = os.getenv("mongodb_password")

uri = f"mongodb+srv://dokyung36d:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile = ca)

embedding_model = OpenAIEmbeddings(api_key=openai_key)

# VectorStore 초기화
database="RAG"
collection="embedding"
key="hobby"
num_fetched=1
index_name="hobby_index"

vector_store = MongoDBAtlasVectorSearch(
    collection=client[database][collection],
    embedding=embedding_model,
    text_key="page_content",
    index_name=index_name,
    embedding_key="hobby_embedding",
    relevance_score_fn="cosine"
)

def fetch_relevant_document(query_text, num_fetched=5):
    """
    텍스트 쿼리를 기반으로 유사한 문서 검색
    - query_text: 검색할 텍스트
    - num_fetched: 반환할 문서 수
    """

    # Langchain 내장 similarity_search 사용
    similar_docs = vector_store.similarity_search(query_text, k=num_fetched)

    # 결과에서 필요한 필드 추출 (예: 문서 전체 내용 혹은 특정 메타데이터 등)
    # 필요한 key가 있다면 아래를 수정
    retrieved_hobby_list = [doc.page_content for doc in similar_docs]

    return retrieved_hobby_list

print(fetch_relevant_document("outdoor activities"))


# from pymongo import MongoClient
# import os
# import certifi

# ca = certifi.where()
# mongodb_password = os.getenv("mongodb_password")

# uri = f"mongodb+srv://dokyung36d:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(uri, tlsCAFile=ca)

# db = client["newspaperTitle"]
# collection = db['title']

# # 모든 문서를 순회하면서 구조 변경
# for doc in collection.find({}):
#     updated_doc = {
#         "page_content": doc["newspaper_title"],
#         "metadata": {
# },
#         "hobby_embedding": doc['hobby_embedding']
#     }
#     # 기존 문서 교체 (upsert=False로 문서 덮어쓰기)
#     collection.replace_one({"_id": doc["_id"]}, updated_doc)

# print("데이터 구조 업데이트 완료")