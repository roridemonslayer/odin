#odins connectiont to the brain
import json #converts human text to json data 
import urllib.request 
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:4b-instruct"

#this is goign to take in messages to send
def chat(messages): 
    body = {  #<- what ollama needs
        "model": MODEL, 
        "messages" : messages, 
        "stream": False,
    }
    data = json.dumps(body).encode()

    req = urllib.request.Request(OLLAMA_URL, data = data, headers = {"Content-Type" : "application/json"})

    with urllib.request.urlopen(req) as resp: 
        result = json.load(resp)
    return result["message"]

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are ODIN. Keep answers short."},
        {"role": "user", "content": "hey odin, who are you?"},
    ]
    reply = chat(messages)
    print(reply["content"])