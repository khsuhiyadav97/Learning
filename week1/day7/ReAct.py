import os
from pathlib import Path
import re
from anyio import sleep
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Api Error, There's no api_key")

client = Groq(api_key = my_api_key)

model = "openai/gpt-oss-120b"

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

        response = client.chat.completions.create(model="openai/gpt-oss-120b", messages= messages, temperature=0)
        answer = response.choices[0].message.content

        print(answer)

        #Agent has finished
        if "final_answer:" in answer:
            break

        #Find the action

        match = re.search(
            r"Action:\s*(\w+)\((.*?)\)",
            answer
        )

        if match:

            tool_name = match.group(1)
            tool_input = match.group(2)
            tool_input = match.input.strip()
            tool_input = match.input.strip('"')

            #Run the tool
            if tool_name in tools:

                tool = tools[tool_name]
                observation = tool(tool_input)

            else:
                observation = "Tool not found"

            print("Observation:", observation)

            #Ask LLM response to memory

            messages.append({
                "role": "assistant",
                "content": answer
            })

            #Give ttool results back to the agent

            messages.append({
                "role": "user",
                "content": "Observation: "+ str(observation)
            })
            sleep(5)

prompt = """I have 200000 ruppees, what is the price of an iphone16?
and how much money will I have left?
"""
run_agent(prompt)