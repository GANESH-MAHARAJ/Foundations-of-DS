from flask import Flask, request, jsonify
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import os


# Set up Flask
app = Flask(__name__)

# Set your OpenAI API key
apikey = os.getenv("OPENAI_API_KEY")
print(f"API KEY: '{apikey}'")

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key=apikey,
    organization="org-VjmGDwVDjBBnBivJtIX3VFek"
)

# Store memory per user to maintain context
user_memories = {}

# def get_chain(user_id):
    # if user_id not in user_memories:
    #     memory = ConversationBufferMemory(return_messages=True)
    #     chain = ConversationChain(llm=llm, memory=memory, verbose=True)
    #     user_memories[user_id] = chain
    # return user_memories[user_id]
    
def get_chain(user_id):
    if user_id not in user_memories:
        memory = ConversationBufferMemory(return_messages=True)

        # Add a system prompt to focus the conversation on movies only
        prompt = PromptTemplate.from_template("""
        You are MovieChatBot, an intelligent assistant who is an expert in movies and TV shows.
        You answer questions **only related to movies**, including actors, genres, plots, ratings, directors, awards, etc.
        If the user asks something unrelated to movies or TV shows, politely inform them that you can only help with movie-related queries.
        
        Current conversation:
        {history}
        Human: {input}
        AI:
        """)

        chain = ConversationChain(
            llm=llm,
            memory=memory,
            prompt=prompt,
            verbose=True
        )

        user_memories[user_id] = chain
    return user_memories[user_id]


@app.route("/generate", methods=["POST"])
def generate_response():
    try:
        user_message = request.json.get("message")
        sender_id = request.json.get("sender", "default_user")

        if not user_message:
            return jsonify({"response": "No message provided."})

        print(f"[{sender_id}] User: {user_message}")

        chain = get_chain(sender_id)
        response = chain.run(user_message)

        print(f"[{sender_id}] Bot: {response}")
        return jsonify({"response": response})

    except Exception as e:
        print("❌ Error in /generate:", str(e))
        return jsonify({"response": "LangChain server error."})

if __name__ == "__main__":
    app.run(port=8081)
