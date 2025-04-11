import requests

msg = {"message": "Tell me about Inception"}

res = requests.post("http://localhost:8082/chat", json=msg)
print("Status:", res.status_code)
print("Response:", res.text)
