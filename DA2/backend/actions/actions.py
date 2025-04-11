from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import pandas as pd
from typing import Text, List, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from fuzzywuzzy import process

llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

class ActionMovieChat(Action):
    def name(self):
        return "action_movie_chat"

    def run(self, dispatcher, tracker, domain):
        movie_name = tracker.get_slot("movie")
        movie_info = df[df["Title"].str.lower() == movie_name.lower()]

        if not movie_info.empty:
            description = movie_info["Short Description"].values[0]
            user_query = tracker.latest_message.get("text")

            prompt = [
                SystemMessage(content="You are a helpful movie expert."),
                HumanMessage(content=f"Tell me about {movie_name}: {description}. User asked: {user_query}")
            ]
            
            response = llm(prompt)
            dispatcher.utter_message(text=response.content)
        else:
            dispatcher.utter_message(text="I couldn't find that movie.")

        return []

class ActionRememberMovie(Action):
    def name(self):
        return "action_remember_movie"

    def run(self, dispatcher, tracker, domain):
        movie_name = tracker.get_slot("movie")
        return [SlotSet("last_movie", movie_name)]


# Load movie data safely
MOVIE_DATA_PATH = "mov_data.csv"

df = pd.read_csv(MOVIE_DATA_PATH)

# Ensure column names are stripped of whitespace
df.columns = df.columns.str.strip()

# Convert necessary columns to correct data types
df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce").fillna(0).astype(int)
df["IMDb Rating"] = pd.to_numeric(df["IMDb Rating"], errors="coerce").fillna(0)
df["Metascore"] = pd.to_numeric(df["Metascore"], errors="coerce").fillna(0)
df["Runtime"] = pd.to_numeric(df["Runtime"], errors="coerce").fillna(0)
df["Title"] = df["Title"].astype(str)

def safe_extract(match):
    if match and len(match) >= 2:
        return match[0], match[1]
    return None, 0

class ActionGetMovieDetails(Action):
    def name(self) -> Text:
        return "action_get_movie_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        movie_name = next(tracker.get_latest_entity_values("movie_name"), None)

        if movie_name:
            match = process.extractOne(movie_name, df["Title"])
            best_match, score = safe_extract(match)
            if best_match and score > 75:
                details = df[df["Title"] == best_match].iloc[0]
                response = (
                    f"🎬 *{details['Title']}* ({details['YEAR']})\n"
                    f"⭐ IMDb: {details['IMDb Rating']}/10\n"
                    f"⏳ Runtime: {details['Runtime']} min\n"
                    f"🔖 Metascore: {details['Metascore']}\n"
                    f"🎟 MPAA: {details.get('MPAA Rating', 'N/A')}\n"
                    f"📖 Description: {details.get('Short Description', 'No description available.')}"
                )
            else:
                response = f"❌ Sorry, I couldn't find '{movie_name}'. Try another movie."
        else:
            response = ""

        dispatcher.utter_message(text=response)
        return []

class ActionGetTopMovies(Action):
    def name(self) -> Text:
        return "action_get_top_movies"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        top_movies = df.nlargest(5, "IMDb Rating")[["Title", "YEAR", "IMDb Rating"]]

        if not top_movies.empty:
            response = "🎥 Here are the top-rated movies:\n" + "\n".join(
                [f"{i+1}. *{row['Title']}* ({row['YEAR']}) - ⭐ {row['IMDb Rating']}" for i, row in top_movies.iterrows()]
            )
        else:
            response = ""

        dispatcher.utter_message(text=response)
        return []

class ActionGetMoviesByYear(Action):
    def name(self) -> Text:
        return "action_get_movies_by_year"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        year = next(tracker.get_latest_entity_values("year"), None)

        if year and year.isdigit():
            year = int(year)
            movies = df[df["YEAR"] == year][["Title", "IMDb Rating"]]

            if not movies.empty:
                response = f"📅 Movies from {year}:\n" + "\n".join(
                    [f"🎬 *{row['Title']}* - ⭐ {row['IMDb Rating']}" for _, row in movies.iterrows()]
                )
            else:
                response = f"❌ No movies found for {year}."
        else:
            response = ""

        dispatcher.utter_message(text=response)
        return []

class ActionGetMoviesByMPAARating(Action):
    def name(self) -> Text:
        return "action_get_movies_by_mpaa_rating"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mpaa_rating = next(tracker.get_latest_entity_values("mpaa_rating"), None)

        if mpaa_rating:
            # Normalize MPAA rating
            df["MPAA Rating"] = df["MPAA Rating"].astype(str).str.strip().str.upper()
            mpaa_rating = mpaa_rating.strip().upper()

            print(f"📢 Debug: Filtering movies with MPAA rating: {mpaa_rating}")

            filtered_movies = df[df["MPAA Rating"] == mpaa_rating][["Title", "MPAA Rating"]].drop_duplicates()

            if not filtered_movies.empty:
                response = f"🎬 Movies with {mpaa_rating} rating:\n" + "\n".join(
                    [f"🎬 *{row['Title']}* ({row['MPAA Rating']})" for _, row in filtered_movies.iterrows()]
                )
            else:
                response = f""
        else:
            response = ""

        dispatcher.utter_message(text=response)
        return []

class ActionGetShortMovies(Action):
    def name(self) -> Text:
        return "action_get_movie_runtime"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        runtime = next(tracker.get_latest_entity_values("runtime"), None)

        if runtime:
            try:
                runtime = int(runtime)  # Convert entity to an integer
            except ValueError:
                dispatcher.utter_message(text="⏳ Please provide a valid runtime in minutes.")
                return []

            print(f"📢 Debug: Filtering movies with Runtime <= {runtime}")

            short_movies = df[df["Runtime"] <= runtime][["Title", "Runtime"]].drop_duplicates()

            if not short_movies.empty:
                response = f"🎥 Movies under {runtime} mins:\n" + "\n".join(
                    [f"🎬 *{row['Title']}* - ⏳ {row['Runtime']} min" for _, row in short_movies.iterrows()]
                )
            else:
                response = f""

        else:
            response = ""

        dispatcher.utter_message(text=response)
        return []

class ActionGetMovieMetascore(Action):
    def name(self) -> Text:
        return "action_get_movie_metascore"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_name = next(tracker.get_latest_entity_values("movie_name"), None)

        if movie_name:
            match = process.extractOne(movie_name, df["Title"])
            best_match, score = safe_extract(match)
            if best_match and score > 75:
                metascore = df[df["Title"] == best_match]["Metascore"].values[0]
                response = f"🎭 Metascore for *{best_match}* is {metascore}."
            else:
                response = f""
        else:
            response = ""

        dispatcher.utter_message(text=response)
        return []

