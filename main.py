from generate_random_hobby_and_newspaper_title import generate_hobby_and_newspaper_tile
from embedding import get_embedding
from fetch_relevant import fetch_relevant_document
from prompt import get_relevant_newspapers
from fastapi import FastAPI
from fastapi.responses import JSONResponse

 
app = FastAPI()

@app.get("/fetch")
async def main(hobby, newspaper_title):
    generated_newspaper_title_embedding = get_embedding(newspaper_title)

    retreived_hobby = fetch_relevant_document(generated_newspaper_title_embedding, database="RAG", collection="embedding", key="hobby", num_fetched=1)

    result = get_relevant_newspapers(retreived_hobby, newspaper_title)
 
    RAG_dict = {"retrieved hobby" : retreived_hobby, "relevent newspapers" : result}
    return JSONResponse(content=RAG_dict)