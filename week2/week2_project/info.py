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

Resume = """
# peronal info later 
# : Structure your personal data (skills, projects, education, experience) into a format like JSON so the AI can process it."""

def ask_llm(system_prompt, user_prompt):
    system_message = {
        "role" : "system",
        "content" : "system_prompt"
    }
    user_message = {
        "role" : "user",
        "content" : "user_prompt"
    }
