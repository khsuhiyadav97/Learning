import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Api Error, There's no api_key")

client = Groq(api_key = my_api_key)

model = "qwen/qwen3.6-27b"
role = "user"
prompt = "Tell me a food company name"

message_system = {
    "role" : "system",
    "content" : "You are a brand manager who suggests my food company name, name should be in one word suggest only one name"
}
message = {
    "role" : role,
    "content" : prompt
}

messages = [message_system, message]
response = client.chat.completions.create(model = model, messages = messages, temperature=1) #temperature is 0 by default
#print(response)

print("#########################################################")

answer = response.choices[0].message.content
print(answer)