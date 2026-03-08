# from key import openai_key
from openai import OpenAI
import os

openai_key = os.getenv("openai_key")

openai_org_id = os.getenv("openai_org_id")

client = OpenAI(
  organization=openai_org_id,
  api_key=openai_key
)


def get_embedding(text):
    responese = client.embeddings.create(
    model="text-embedding-ada-002",
    input=text,
    encoding_format="float"
    )

    return responese.data[0].embedding