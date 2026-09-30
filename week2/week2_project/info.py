import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv('GROQ_API_KEY')

if not my_api_key:
    raise ValueError("API error: There's no API key")

client = Groq(api_key = my_api_key)

model = "qwen/qwen3.8-27b"
role = "user"