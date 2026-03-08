from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
import os
import certifi
import time

ca = certifi.where()

openai_key = os.getenv("openai_key")
mongodb_password = os.getenv("mongodb_password")

try:
    embedding_model = OpenAIEmbeddings(api_key=openai_key)
    uri = f"mongodb+srv://dokyung36d:{mongodb_password}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=ca)
except Exception:
    embedding_model = None
    client = None

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


# ─────────────────────────────────────────────────────────────────────────────
# 검색 방식 비교 함수
#
# ANN  (Approximate Nearest Neighbor): 인덱스를 활용한 근사 검색. 빠르지만 결과가
#       완전히 정확하지 않을 수 있음. 대규모 데이터에서 실용적인 선택.
#
# Full Scan (Exact Search): 모든 문서를 직접 벡터 계산하여 정확한 결과 반환.
#       데이터가 많을수록 느려지지만 결과는 완전히 정확함.
#
# 사용법:
#   compare_ann_vs_full_scan("user query", database="db", collection="col",
#                            num_fetched=5, index_name="my_index")
# ─────────────────────────────────────────────────────────────────────────────

def _run_ann_search(vector_store, query_text, num_fetched):
    """ANN 검색 (MongoDB Atlas Vector Index 사용)"""
    docs = vector_store.similarity_search(query_text, k=num_fetched)
    return [doc.page_content for doc in docs]


def _run_full_scan_search(collection, query_vector, num_fetched, index_name):
    """Exact Search (MongoDB $vectorSearch exact: true — 인덱스 없이 전체 벡터 직접 비교)"""
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "index": index_name,
                "path": "hobby_embedding",
                "queryVector": query_vector,
                "exact": True,
                "limit": num_fetched
            }
        },
        {
            "$project": {"page_content": 1, "_id": 0}
        }
    ])
    return [doc.get("page_content", "") for doc in results]


def compare_ann_vs_full_scan(query_text, database, collection, num_fetched, index_name):
    """
    ANN 검색과 Full Scan 검색의 결과 및 소요 시간을 비교 출력합니다.

    Args:
        query_text  : 검색 쿼리 문자열
        database    : MongoDB 데이터베이스 이름
        collection  : MongoDB 컬렉션 이름
        num_fetched : 반환할 문서 수 (top-k)
        index_name  : Atlas Vector Search 인덱스 이름 (ANN에서 사용)

    Returns:
        dict: {"ann": [...], "full_scan": [...]}
    """
    col = client[database][collection]

    vector_store = MongoDBAtlasVectorSearch(
        collection=col,
        embedding=embedding_model,
        text_key="page_content",
        index_name=index_name,
        embedding_key="hobby_embedding",
        relevance_score_fn="cosine"
    )

    # 쿼리 벡터는 두 방식에서 공통으로 한 번만 생성
    query_vector = embedding_model.embed_query(query_text)

    # ── ANN 검색 ──
    start = time.perf_counter()
    ann_results = _run_ann_search(vector_store, query_text, num_fetched)
    ann_elapsed = time.perf_counter() - start

    # ── Full Scan 검색 ──
    start = time.perf_counter()
    full_scan_results = _run_full_scan_search(col, query_vector, num_fetched, index_name)
    full_scan_elapsed = time.perf_counter() - start

    # ── 결과 출력 ──
    print("=" * 60)
    print(f"  검색 방식 비교  |  query: '{query_text}'")
    print("=" * 60)

    print(f"\n[ANN Search]  소요 시간: {ann_elapsed:.4f}s")
    for i, doc in enumerate(ann_results, 1):
        print(f"  {i}. {doc}")

    print(f"\n[Full Scan]   소요 시간: {full_scan_elapsed:.4f}s")
    for i, doc in enumerate(full_scan_results, 1):
        print(f"  {i}. {doc}")

    faster = "ANN" if ann_elapsed < full_scan_elapsed else "Full Scan"
    ratio = max(ann_elapsed, full_scan_elapsed) / min(ann_elapsed, full_scan_elapsed)
    print(f"\n  → {faster}이 {ratio:.1f}배 더 빠름")
    print("=" * 60)

    return {"ann": ann_results, "full_scan": full_scan_results}


if __name__ == "__main__":
    from key import openai_key as _ok, mongodb_password as _mp
    os.environ["openai_key"] = _ok
    os.environ["mongodb_password"] = _mp

    # 환경변수 세팅 후 재초기화
    embedding_model = OpenAIEmbeddings(api_key=_ok)
    uri = f"mongodb+srv://dokyung36d:{_mp}@cluster0.w5p7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=ca)

    compare_ann_vs_full_scan(
        query_text="User's hobby is travel and he is reading newspaper which name is 항공 특가",
        database="newspaperTitle",
        collection="title",
        num_fetched=5,
        index_name="title_vector_index"
    )