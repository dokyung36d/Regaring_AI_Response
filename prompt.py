import json
import random
from embedding import get_embedding
from fetch_relevant import fetch_relevant_document
from openai import OpenAI
from key import openai_key


def get_relevant_newspapers(hobby, newspaper_title):
    prompt = f"User's hobby is {hobby} and he is reading newspaper which name is {newspaper_title}"
    prompt_embedding = get_embedding(prompt)

    fetched_newspapers = fetch_relevant_document(prompt_embedding, database="newspaperTitle", collection="title", key = "newspaper_title", num_fetched=5)

    return fetched_newspapers


def get_recommend_advertise(hobby, newspaper_title, relevent_newspaper):
    client = OpenAI(
    organization='org-RSWEbMw552t3xBqgzkF6w547',
    api_key=openai_key
    )

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {"role": "user", "content": f"the current user's hobby is {hobby}. and he is watching newspaper and its title is {newspaper_title}. relevent newspapers are {relevent_newspaper}. please generate only one advertise words that is directly relevent to hobby and newspaper"},
                {"role": "user", "content": "for example, if the user's hobby is travel, and newspaper title is korean air's new air plane. then generate advertise words such as great discount in singapore airline"},
                {"role": "user", "content": "Please only generate advertise words, and generate in korean"},
                {"role": "user", "content": "Do not generate Sure, here are a few examples: or similar things and only generate 1"}],
        stream=True
    )

    generated_advertise_words = ""

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            # print(chunk.choices[0].delta.content, end="")
            generated_advertise_words += chunk.choices[0].delta.content

    return generated_advertise_words