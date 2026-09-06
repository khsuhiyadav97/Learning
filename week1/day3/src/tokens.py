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
# Multiple prompts
prompt1 = "Hi"
prompt2 = "Explain Natural Language Processing(NLP) in 50 words"
prompt3 = "What is Blackhole?"

prompts = [prompt1, prompt2, prompt3]
for prompt in prompts:
    message={
        "role" : role,
        "content" : prompt
    }
    messages = [message]
    # messages = [message_system, message]
    response = client.chat.completions.create(model = model, messages = messages) #temperature is 0 by default
    usage = response.usage
    print(f"Prompt: {prompt} --> your tokens: {usage.prompt_tokens} -- completion tokens: {usage.completion_tokens} --total tokens: {usage.total_tokens}")

# message = {
#     "role" : role,
#     "content" : prompt
# }

# messages = [message_system, message]
# response = client.chat.completions.create(model = model, messages = messages, temperature=1) #temperature is 0 by default
#print(response)

# print("#########################################################")

# answer = response.choices[0].message.content
# print(answer)