from key import openai_key

from openai import OpenAI

client = OpenAI(
  organization='org-RSWEbMw552t3xBqgzkF6w547',
  api_key=openai_key
)


def get_embedding(text):
    responese = client.embeddings.create(
    model="text-embedding-ada-002",
    input=text,
    encoding_format="float"
    )

    return responese.data[0].embedding