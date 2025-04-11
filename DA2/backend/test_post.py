import requests

url = "http://127.0.0.1:8081/generate"
data = {"message": "Tell me about The Godfather"}

res = requests.post(url, json=data)

# Debug prints
print("Status Code:", res.status_code)
print("Raw Response:", res.text)

try:
    print("Parsed JSON:", res.json())
except Exception as e:
    print("JSON Decode Error:", e)
