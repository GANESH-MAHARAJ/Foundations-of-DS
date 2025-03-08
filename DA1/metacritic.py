import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL with page number placeholder
BASE_URL = "https://www.metacritic.com/browse/movie/?releaseYearMin=1910&releaseYearMax=2025&page={}"

# Function to extract movie details from a single page
def extract_movies_from_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}  # To prevent getting blocked
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    movies_data = []
    
    movies = soup.find_all("div", class_="c-finderProductCard_info")
    for movie in movies:
        try:
            # Extract Title
            title_tag = movie.find("h3", class_="c-finderProductCard_titleHeading")
            title = title_tag.find_all("span")[1].text.strip() if title_tag else "N/A"
            
            # Extract Year
            year_tag = movie.find("span", class_="u-text-uppercase")
            year = year_tag.text.strip().split()[-1] if year_tag else "N/A"
            
            # Extract Metascore
            metascore_tag = movie.find("div", class_="c-siteReviewScore")
            metascore = metascore_tag.find("span").text.strip() if metascore_tag else "N/A"
            
            
            
            mpaa_rating = "N/A"
            for span in movie.find_all("span"):
                if "Rated" in span.text:
                    mpaa_rating = span.text.replace("Rated", "").strip()
                    break  # Stop once found
                
            # Extract Short Description
            desc_tag = movie.find("div", class_="c-finderProductCard_description")
            description = desc_tag.text.strip() if desc_tag else "N/A"
            
            movies_data.append({
                "Title": title,
                "Year": year,
                "Metascore": metascore,
                "MPAA Rating": mpaa_rating,
                "Short Description": description
            })
        except Exception as e:
            print(f"Error extracting data: {e}")
            continue
    
    return movies_data

# Scrape multiple pages
def scrape_metacritic(pages=5):  
    all_movies = []
    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        url = BASE_URL.format(page)
        movies = extract_movies_from_page(url)
        all_movies.extend(movies)
        time.sleep(1)  
    
    # Save data to CSV
    df = pd.DataFrame(all_movies)
    df.to_csv("metacritic_movies.csv", index=False)
    print("Scraping completed. Data saved to 'metacritic_movies.csv'")
    print(df.shape)
    return df

# Run the scraper
scrape_metacritic(pages=691)  
