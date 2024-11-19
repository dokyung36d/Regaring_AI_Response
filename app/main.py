from generate_random_hobby_and_newspaper_title import generate_hobby_and_newspaper_tile
from embedding import get_embedding
from fetch_relevant import fetch_relevant_document
from prompt import get_relevant_newspapers, get_recommend_advertise
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import redis
import json


##http://127.0.0.1:8000/fetch?hobby=sports&newspaper_title=World%20Cup%20Finals
##uvicorn app.main:app --reload

##http://0.0.0.1:8000/fetch?hobby=sports&newspaper_title=World%20Cup%20Finals
## docker run --env-file .env -p 8000:8000 rag


r = redis.Redis(host='localhost', port=6379, db=0) # 로컬에 띄운 Redis 서버에 연결 

 
app = FastAPI()

@app.get("/fetch")
async def main(hobby, newspaper_title):
    key = json.dumps({"hobby" : hobby, "newspaper_title" : newspaper_title})

    if r.get(key) is not None:
       return JSONResponse(content=json.loads(r.get(key))) 
    generated_newspaper_title_embedding = get_embedding(newspaper_title)

    retreived_hobby = fetch_relevant_document(generated_newspaper_title_embedding, database="RAG", collection="embedding", key="hobby", num_fetched=1)

    relevent_newspapers = get_relevant_newspapers(retreived_hobby, newspaper_title)
    recommended_advertise = get_recommend_advertise(hobby, newspaper_title, relevent_newspapers)
 
    RAG_dict = {"relevent hobby" : retreived_hobby, "relevent newspapers" : relevent_newspapers, "recommended_advertise" : recommended_advertise}
    RAG_dict_JSON = json.dumps(RAG_dict)
    r.set(key, RAG_dict_JSON)

    return JSONResponse(content=RAG_dict)