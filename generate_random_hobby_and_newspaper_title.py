from key import openai_key
import json

from openai import OpenAI

def generate_hobby_and_newspaper_tile():

    client = OpenAI(
    organization='org-RSWEbMw552t3xBqgzkF6w547',
    api_key=openai_key
    )

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hi my name is dokyung"},
                {"role": "assistant", "content": "Hi Dokyung! How can I assist you today?"},
                {"role": "user", "content": "i want to make an data. Generate the hobby"},
                {"role": "user", "content": "Please only generate hobbye"},
                {"role": "user", "content": "Do not generate Sure, here are a few examples: or similar things and only generate 1"}],
        stream=True,
    )

    generated_hobby = ""

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            # print(chunk.choices[0].delta.content, end="")
            generated_hobby += chunk.choices[0].delta.content

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hi my name is dokyung"},
                {"role": "assistant", "content": "Hi Dokyung! How can I assist you today?"},
                {f"role": "user", "content": "i want to make an data. Generate the newspaper title that is relevant to {generated_hobby}"},
                {"role": "user", "content": "Please only generate newspaper title"},
                {"role": "user", "content": "Do not generate Sure, here are a few examples: or similar things and only generate 1, do not include ''"}],
        stream=True,
    )

    generated_newspaper_title = ''

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            # print(chunk.choices[0].delta.content, end="")
            generated_newspaper_title += chunk.choices[0].delta.content

    # Output the dictionary
    
    return generated_hobby, generated_newspaper_title