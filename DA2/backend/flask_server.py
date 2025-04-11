from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
RASA_API = "http://localhost:5005/webhooks/rest/webhook"
LANGCHAIN_API = "http://localhost:8081/generate"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    print(f"\n>>> Received message: {user_input}")

    try:
        rasa_response = requests.post(RASA_API, json={"message": user_input}).json()
        print("RASA response:", rasa_response)
        
        if rasa_response:
            text_reply = " ".join([msg["text"] for msg in rasa_response if "text" in msg])
            return jsonify({"response": text_reply})

        langchain_response = requests.post(LANGCHAIN_API, json={"message": user_input}).json()
        print("LangChain response:", langchain_response)
        return jsonify(langchain_response)
    
    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": "Server error"}), 500

if __name__ == "__main__":
    app.run(port=8082)
