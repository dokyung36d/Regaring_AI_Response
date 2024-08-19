from key import openai_key

from openai import OpenAI

client = OpenAI(
  organization='org-RSWEbMw552t3xBqgzkF6w547',
  api_key=openai_key
)

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "can you tell me about ha-seong kim?"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")