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
parser.add_argument('--logs', help="Where to store logs.")

def ask_question(msgs, model):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msgs
    )

def extract_reply(res):
    return res['choices'][0]['message']

def log_out(string, handle):
    if handle != None:
        handle.writelines([string])
        handle.flush()

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

    file_path = args.get("logs")
    log_handle = None
    if file_path != None:
        log_handle = open(file_path, "w", encoding="utf-8")

    cur_messages = [
            {"role": "system", "content": "You are a helpful assistant. Please respond using a standard markdown format and incorporate formatting, headings, and any other text elements to make your responses more engaging."}
        ]
    user_in = ""
    print("ChatGPT Command Line Test")
    
    try:
        while True:
            user_in = input("> ")
            if user_in == "quit":
                break
            cur_messages.append({"role": "user", "content": user_in})
            log_out(f"USER: {user_in}\n",log_handle)
            res = ask_question(cur_messages,model)
            reply = extract_reply(res)
            reply_content = reply["content"]
            log_out(f"GPT: { reply_content }\n",log_handle)
            print(reply_content)
            cur_messages.append(reply)
    except:
        log_handle.close()

if __name__ == "__main__":
    main()