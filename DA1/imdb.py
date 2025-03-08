import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.imdb.com/chart/top/"

# Set up Selenium WebDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in the background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open IMDb page
driver.get(URL)
time.sleep(5)  # Wait for JavaScript to load

# Scroll down to load all movies
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Parse page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract movie elements
movies = soup.select(".ipc-metadata-list-summary-item")
movie_data = []

for movie in movies:
    title = movie.select_one("h3").text.strip() if movie.select_one("h3") else "N/A"
    details = movie.select("span.sc-b189961a-8")
    
    metadata_spans = movie.select("span.sc-d5ea4b9d-7")  # Select all spans inside the metadata div

    year = metadata_spans[0].text.strip() if len(metadata_spans) > 0 else "N/A"
    runtime = metadata_spans[1].text.strip() if len(metadata_spans) > 1 else "N/A"
    
    # year = details[0].text.strip("()") if len(details) > 0 else "N/A"
    # year = movie.select_one(".ipc-inline-list__item").text.strip() if movie.select_one(".ipc-inline-list__item") else "N/A"
    # runtime = details[1].text.strip() if len(details) > 1 else "N/A"
    
    rating = movie.select_one("span.ipc-rating-star").text.strip() if movie.select_one("span.ipc-rating-star") else "N/A"
    votes = movie.select_one("span.ipc-rating-star--voteCount").text.strip("()") if movie.select_one("span.ipc-rating-star--voteCount") else "N/A"



    movie_data.append([title, year, rating, runtime, votes])

# Close WebDriver
driver.quit()

# Convert to DataFrame
imdb_df = pd.DataFrame(movie_data, columns=["Title", "Year", "IMDb Rating", "Runtime", "Votes"])
imdb_df.to_csv("imdb.csv", index=False)

# Output
print(imdb_df.head())
print(f"Total movies scraped: {imdb_df.shape[0]}")
