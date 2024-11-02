# from key import openai_key
import json
import random
import os

from openai import OpenAI

openai_key = os.getenv("openai_key")

def generate_hobby_and_newspaper_tile():
    seed = random.randint(1, 10000)

    client = OpenAI(
    organization='org-RSWEbMw552t3xBqgzkF6w547',
    api_key=openai_key
    )

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {"role": "user", "content": "i want to make an data. Generate the hobby, but not photography"},
                {"role": "user", "content": "Please only generate hobby"},
                {"role": "user", "content": "Do not generate Sure, here are a few examples: or similar things and only generate 1"}],
        stream=True,
        seed = seed
    )

    generated_hobby = ""

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            # print(chunk.choices[0].delta.content, end="")
            generated_hobby += chunk.choices[0].delta.content

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {f"role": "user", "content": "i want to make an data. Generate the newspaper title that is directly relevant to {generated_hobby}, and include that hobby in that title"},
                {"role": "user", "content": "Please only generate newspaper title"},
                {"role": "user", "content": "Do not generate Sure, here are a few examples: or similar things and only generate 1, do not include ''"}],
        stream=True,
        seed = seed
    )

    generated_newspaper_title = ''

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            # print(chunk.choices[0].delta.content, end="")
            generated_newspaper_title += chunk.choices[0].delta.content

    # Output the dictionary
    
    return generated_hobby, generated_newspaper_title