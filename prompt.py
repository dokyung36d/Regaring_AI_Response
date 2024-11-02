from key import openai_key
import json
import random
from embedding import get_embedding
from fetch_relevant import fetch_relevant_document
from openai import OpenAI


def get_relevant_newspapers(hobby, newspaper_title):
    prompt = f"User's hobby is {hobby} and he is reading newspaper which name is {newspaper_title}"
    prompt_embedding = get_embedding(prompt)

    fetched_newspapers = fetch_relevant_document(prompt_embedding, database="newspaperTitle", collection="title", key = "newspaper_title", num_fetched=5)

    return fetched_newspapers


    