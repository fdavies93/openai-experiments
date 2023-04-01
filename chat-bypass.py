import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

def ask_question(msgs):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msgs
    )

def extract_reply(res):
    return res['choices'][0]['message']

cur_messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
user_in = ""
print("ChatGPT Command Line Test")
while True:
    user_in = input("> ")
    if user_in == "quit":
        break
    cur_messages.append({"role": "user", "content": user_in})
    res = ask_question(cur_messages)
    reply = extract_reply(res)
    print(reply["content"])
    cur_messages.append(reply)