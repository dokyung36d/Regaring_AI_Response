from generate_random_hobby_and_newspaper_title import generate_hobby_and_newspaper_tile
from embedding import get_embedding
from fetch_relevant import fetch_relevant_document
from prompt import get_relevant_newspapers, get_recommend_advertise
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import redis
import json
import re


##http://127.0.0.1:8000/fetch?hobby=sports&newspaper_title=World%20Cup%20Finals
##uvicorn app.main:app --reload

##http://0.0.0.1:8000/fetch?hobby=sports&newspaper_title=World%20Cup%20Finals
## docker run --env-file .env -p 8000:8000 rag


r = redis.Redis(host='localhost', port=6379, db=0) # 로컬에 띄운 Redis 서버에 연결 

 
app = FastAPI()

_MAX_INPUT_LEN = 200
_BLOCKED_PATTERN = re.compile(
    r"(ignore (previous|above|all) instructions?|forget (previous|all)|"
    r"system prompt|you are now|act as|disregard|override)",
    re.IGNORECASE,
)

def _validate_input(value: str, field: str) -> str:
    value = value.strip()
    if len(value) > _MAX_INPUT_LEN:
        raise HTTPException(status_code=400, detail=f"{field} must be {_MAX_INPUT_LEN} characters or fewer")
    if _BLOCKED_PATTERN.search(value):
        raise HTTPException(status_code=400, detail=f"Invalid input in {field}")
    return value

@app.get("/fetch")
async def main(hobby, newspaper_title):
    hobby = _validate_input(hobby, "hobby")
    newspaper_title = _validate_input(newspaper_title, "newspaper_title")
    key = json.dumps({"hobby" : hobby, "newspaper_title" : newspaper_title})

    if r.get(key) is not None:
       return JSONResponse(content=json.loads(r.get(key))) 

    retreived_hobby = fetch_relevant_document(newspaper_title, database="RAG", collection="embedding", num_fetched=1, index_name="hobby_index")

    relevent_newspapers = get_relevant_newspapers(retreived_hobby, newspaper_title)
    recommended_advertise = get_recommend_advertise(hobby, newspaper_title, relevent_newspapers)
 
    RAG_dict = {"relevent hobby" : retreived_hobby, "relevent newspapers" : relevent_newspapers, "recommended_advertise" : recommended_advertise}
    RAG_dict_JSON = json.dumps(RAG_dict)
    r.set(key, RAG_dict_JSON)

    return JSONResponse(content=RAG_dict)