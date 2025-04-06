# 🎬 Movie Chatbot using RASA and LangChain

A smart, context-aware chatbot designed to answer user queries about movies and TV shows. Built as part of the **Foundations of Data Science (BCS206L)** course at **VIT Vellore**.

## 📌 Overview

This chatbot integrates two powerful NLP tools:
- **RASA**: For intent classification, entity extraction, and rule-based response generation.
- **LangChain + GPT**: For natural, free-form, and context-aware text generation when RASA cannot resolve a query.

The chatbot runs on a **React + Flask** stack, delivering responses through a clean, user-friendly web interface.

## 📂 Features

✅ Intent Recognition using RASA NLU  
✅ Entity Extraction from custom movie dataset  
✅ Conversational context handling  
✅ Dynamic fallback response generation using LangChain and GPT-4  
✅ Integrated frontend + backend with real-time chat interface

## 🛠️ Tech Stack

- **Frontend**: React + Vite  
- **Backend**: Flask (Python)  
- **NLP Engines**: RASA, LangChain (with OpenAI GPT)  
- **Dataset**: Custom CSV of movies and TV shows  
- **Environments**:
  - `rasa_env` for all RASA-related dependencies
  - `langchain_env` for LangChain + GPT integration

## 🚀 Project Structure

📁 backend/ ├── flask_server.py # Main Flask app └── langchain_server.py # LangChain GPT handler

📁 frontend/ ├── Chatbot.jsx # Chat UI component ├── App.jsx # Root component └── index.css # Styling

📁 rasa_project/ ├── domain.yml ├── data/nlu.yml ├── data/rules.yml ├── data/stories.yml └── actions.py


## 📽️ Demo Video

🎥 YouTube Playlist: [Click here to view demo](https://youtube.com/playlist?list=PLGDxwdLu472oJnUqcB_pJiFHXkWZBgEoy&si=zeswO2st7Rcjrcx7)  


## 📊 Dataset

Custom dataset scraped from multiple sources and structured into `mov_data.csv`.  
Columns include:  
- Title  
- Genre  
- Year  
- Language  
- Cast  
- Rating  
- Platform

## 📦 Installation Instructions

> Make sure to use two virtual environments: one for `RASA` and one for `LangChain`.

1. **Clone the repo**

git clone https://github.com/your-username/movie-chatbot-rasa-langchain.git
cd movie-chatbot-rasa-langchain

2. Run RASA server

rasa train (if models dir not downloaded)
rasa run --enable-api --cors "*" --debug
rasa run actions (in another terminal)

3. Run LangChain server

python langchain_server.py

4.Run Flask server (proxy backend)

python flask_server.py

5. Run Frontend

npm install
npm run dev

🙋‍♂️ Author
Ganeshmaharaj K
Student – B.Tech CSE (DS), VIT Vellore
Semester: Winter 2024–25
Email: ganeshmaharaj.kamatham@email.com 

📃 License
This project is for academic purposes only and is not licensed for commercial use.









