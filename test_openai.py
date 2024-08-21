from key import openai_key

from openai import OpenAI

client = OpenAI(
  organization='org-RSWEbMw552t3xBqgzkF6w547',
  api_key=openai_key
)

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hi my name is dokyung"},
              {"role": "assistant", "content": "Hi Dokyung! How can I assist you today?"},
              {"role": "user", "content": "do you remember my name?"},
              {"role": "assistant", "content": "Hi Dokyung! How can I assist you today?"},
              {"role": "user", "content": "is there any flight from incheon to istanbul in 2022?"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")