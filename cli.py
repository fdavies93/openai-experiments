import openai
import os
import json
from dotenv import load_dotenv
import argparse

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

parser = argparse.ArgumentParser(description="Simple CLI interface to OpenAI APIs.")
parser.add_argument('--models', help="Get list of models and exit.", action="store_true")
parser.add_argument('--model', help="Select model.")

def ask_question(msgs, model):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msgs
    )

def extract_reply(res):
    return res['choices'][0]['message']

def main():
    args = vars(parser.parse_args())
    
    if args.get("models"):
        models_res = openai.Model.list()["data"]
        model_list = [model["id"] for model in models_res]
        print(f"Models available: {', '.join(model_list)}")
        return

    model = args.get("model")

    if model == None:
        model = "gpt-3.5-turbo"

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
        res = ask_question(cur_messages,model)
        reply = extract_reply(res)
        print(reply["content"])
        cur_messages.append(reply)

if __name__ == "__main__":
    main()