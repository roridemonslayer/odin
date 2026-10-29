#here we are goign to do our looping
from llm import chat

messages =[
    {"role": "system", "content": "You are ODIN. Keep your answers short for now"},
   
]
while True: 
    text = input("You: ") #takes in ur input
    if text.strip().lower() in ("bye", "exit", "quit"):
        break