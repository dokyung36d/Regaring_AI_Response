from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import certifi
# from key import mongodb_password

ca = certifi.where()

mongodb_password = os.getenv("mongodb_password")

uri = f"mongodb+srv://dokyung36d:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile = ca)

def fetch_relevant_document(embedding, database, collection, key, num_fetched, index_name):
    db = client[database]
    collection = db[collection]

    pipeline = [
        {
            "$vectorSearch": {
                "index": index_name,  # Atlas에서 설정한 인덱스 이름으로 변경 필요
                "path": "hobby_embedding",      # 벡터 필드 이름
                "queryVector": embedding,       # 검색 쿼리 벡터
                "numCandidates": 100,            # 후보군 개수 (적절히 조절 가능)
                "limit": num_fetched,            # 최종 반환 개수
                "similarity": "cosine"           # 유사도 방식 (cosine, euclidean 등)
            }
        },
        {
            "$project": {
                key: 1,               # 필요한 필드만 선택
            }
        }
    ]

    # 검색 실행
    results = list(collection.aggregate(pipeline))

    # 결과 리스트 구성
    retrieved_hobby_list = [result[key] for result in results]

    return retrieved_hobby_list