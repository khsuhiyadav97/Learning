import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Api Error, There's no api_key")

client = Groq(api_key = my_api_key)

model = "qwen/qwen3.8-27b"
role = "user"
prompt = "Do you know how RAG works?"
message = {
    "role" : role,
    "content" : prompt
}
messages = [message]

print("#########################################################")

stream = client.chat.completions.create(model= model, messages= messages, stream= True)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end=" ", flush=True);