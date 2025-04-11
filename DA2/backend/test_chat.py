import requests

URL = "http://localhost:8082/chat"

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    response = requests.post(URL, json={"message": user_input})
    print(response.json())
