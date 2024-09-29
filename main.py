from generate_random_hobby_and_newspaper_title import generate_hobby_and_newspaper_tile
from embedding import get_embedding
from fetch_relevant import fetch_relevant_document

generated_hobby, generated_newspaper_title = generate_hobby_and_newspaper_tile()

generated_newspaper_title_embedding = get_embedding(generated_newspaper_title)

retreived_name, retreived_hobby = fetch_relevant_document(generated_newspaper_title_embedding)

print(f"generated hobby : {generated_hobby}, generated newspaper title : {generated_newspaper_title}")

print(retreived_name)
print(retreived_hobby)