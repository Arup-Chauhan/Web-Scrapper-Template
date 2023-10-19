#Right now it is for the initial inspired idea IMDB-Top 100
# import requests
from bs4 import BeautifulSoup
import pandas as pd

# Grab the top 100 movies from IMDb
url = 'https://www.imdb.com/search/title/?groups=top_100&ref_=adv_prv'
headers = {"Accept-Language": "en-US, en;q=0.5"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Initialize lists to store movie data
movie_name = []
movie_year = []
movie_runtime = []
imdb_ratings = []
metascores = []
number_votes = []
us_gross_millions = []

# Find all movie containers
movie_containers = soup.find_all("div", class_="lister-item mode-advanced")

# Extract data from each movie container
for container in movie_containers:
    # Movie name
    name = container.h3.a.text
    movie_name.append(name)

    # Movie year
    year = container.h3.find("span", class_="lister-item-year").text
    movie_year.append(year)

    # Movie runtime
    runtime = container.find("span", class_="runtime")
    if runtime is not None:
        movie_runtime.append(int(runtime.text.split(" ")[0]))
    else:
        movie_runtime.append(None)

    # IMDb rating
    imdb = float(container.strong.text)
    imdb_ratings.append(imdb)

    # Metascore
    metascore = container.find("span", class_="metascore")
    if metascore is not None:
        metascores.append(int(metascore.text))
    else:
        metascores.append(None)

    # Number of votes
    votes = container.find("span", attrs={"name": "nv"})["data-value"]
    number_votes.append(int(votes))

    # US gross (in millions)
    gross = container.find("span", class_="text-muted text-small")
    if gross is not None and gross.text.strip() != "Gross:":
        us_gross_millions.append(float(gross.text.split("$")[1].split("M")[0]))
    else:
        us_gross_millions.append(None)

# Create a DataFrame from the extracted data
movies = pd.DataFrame({
    "Name": movie_name,
    "Year": movie_year,
    "Runtime (min)": movie_runtime,
    "IMDb Rating": imdb_ratings,
    "Metascore": metascores,
    "Number of Votes": number_votes,
    "US Gross (Millions)": us_gross_millions,
})

# Save the DataFrame to a CSV file
movies.to_csv("top_100_movies.csv", index=False)
