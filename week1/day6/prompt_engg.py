import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Api Error, There's no api_key")

client = Groq(api_key = my_api_key)

model = "openai/gpt-oss-20b"

def llm_call(prompt):
    message = {
        "role" : "user",
        "content" : prompt
    }
    messages = [message]
    response = client.chat.completions.create(model = model, messages = messages)
    answer = response.choices[0].message.content
    return answer

# A good prompt requires six things - Role, Task, Constraints, Output, ZeroShot/Oneshot/Fewshots, and Fallback to understand a problem deeply.

write_prompt = """
# ROLE: You are support assistant at a mobile/laptop company.
# TASK: You have to classify the issue in category.
# Category: You have to classify the issue in three categories- Billing, Techincal, Return.
# OUTPUT: Your answer should be in one word, and it is from the constranits categories.
# Oneshot: For an example: My Laptop screen went black.
# Fallback: If the issue is unrealted then the answer should be OTHER.

This is user complaint: My Laptop is not working """

print(llm_call(write_prompt))
