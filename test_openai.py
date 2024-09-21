from key import openai_key

from openai import OpenAI

client = OpenAI(
  organization='org-RSWEbMw552t3xBqgzkF6w547',
  api_key=openai_key
)

# stream = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[{"role": "user", "content": "Hi my name is dokyung"},
#               {"role": "assistant", "content": "Hi Dokyung! How can I assist you today?"},
#               {"role": "user", "content": "do you remember my name?"},
#               {"role": "assistant", "content": "Hi Dokyung! How can I assist you today?"},
#               {"role": "user", "content": "can you tell me about hyunjin-ryu?"}],
#     stream=True,
# )

# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")

responese = client.embeddings.create(
  model="text-embedding-ada-002",
  input="Turkish Food is Delicious!!",
  encoding_format="float"
)

print("hello world")

print(responese.data[0].embedding)