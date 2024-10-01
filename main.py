from generate_random_hobby_and_newspaper_title import generate_hobby_and_newspaper_tile
from embedding import get_embedding
from fetch_relevant import fetch_relevant_document
from prompt import ge

# generated_hobby, generated_newspaper_title = generate_hobby_and_newspaper_tile()
generated_hobby, generated_newspaper_title = "축구", "손흥민 푸스카스 수상"

generated_newspaper_title_embedding = get_embedding(generated_newspaper_title)

retreived_hobby = fetch_relevant_document(generated_newspaper_title_embedding, database="RAG", collection="embedding", key="hobby", num_fetched=1)

print(f"generated hobby : {generated_hobby}, generated newspaper title : {generated_newspaper_title}")

print(retreived_hobby)

result = ge(retreived_hobby, generated_newspaper_title)

print(result)