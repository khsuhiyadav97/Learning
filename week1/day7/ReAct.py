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

# tools
def product_price(product):
    if product == "iPhone18":
        return 200000
    elif product == "iPhone16":
        return 60000
    else:
        return 0

def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calc_error"

tools = {
    "product_price": product_price,
    "calculator": calculator
}
system_prompt = """
You are a shopping assistant,
You have these tools:
product_price(product)
calculator(expressions)

IMPORTANT:
Call tools exactly like these examples:

Action: product_price("iPhone16")
Action: calculator("60000-100000")

Never write:
product_price(product = "iPhone18")

Never write 
Calculator(expression = "60000-100000")
Follow these rules:

1. Descode what you need to do next.
2. Call only one tool at a time.
3. After writing an action, Stop IMMEDIATELY
4. Never guess or invent a tool or result
5. Wait until you recieve the observation.
6. Then decide you next action.
7. When the task is complete give the final answer.

Format: Thpught what you need to do
Action tool_name(argument)

WHEN FINISHED:
Final answer: ypur answer
"""

def run_agent(question):
    messages = [
        {
            "role": "system",
            "content":system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(5):
        print("----------------/n")
        print("STEP", step+1)
        print("----------------/n")

        response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages= messages, temperature=0)
        answer = response.choices[0].message.content

        print(answer)
