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
# Structured format information

from pydantic import BaseModel
class Ticket(BaseModel):
    name : str
    email : str
    issue : str

schema = Ticket.model_json_schema()

response_format = {
    "type" : "json_object"
}
system_prompt = f"""
Extract the personal information fromt the ticket strictly based on this schema. And provide a json foramt reponse. {schema}
"""

message_system = {
    "role": "system",
    "content": system_prompt
}
text = "Hello My name is Kay. I bought an ipad from your store. It stopped working. I live in Delhi. My email is abc@gmail.com and mobile number is 1234567890."
prompt = f"""
This is a custotmer ticket. Please extract the personal information from this.{text}
"""
message = {
    "role" : role,
    "content" : prompt
}
messages = [message_system, message]
response = client.chat.completions.create(model = model, messages = messages, response_format = response_format)

answer = response.choices[0].message.content
print(answer)

# Load
import json
raw_json = answer
data_file = json.loads(raw_json)
ticket = Ticket(**data_file)

# You can see it directly
print(ticket.name)
print(ticket.email)
print(ticket.issue)
