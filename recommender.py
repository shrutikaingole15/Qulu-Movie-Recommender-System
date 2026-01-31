import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
import requests
import os

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

def load_data():
    # Helper to allow importing without running immediately if needed, 
    # but for this simple assignment, we will execute at module level or
    # keep it simple. However, Streamlit caching works best with functions.
    # To satisfy "App must import recommender.py and reuse its logic" and "clean code",
    # I will make a class or functions? 
    # User said: "Implement function: recommend(movie_title: str) -> list[str]"
    
    # Let's execute the logic at module level so 'recommend' works directly.
    pass

# Load datasets
try:
    movies = pd.read_csv('tmdb_5000_movies.csv')
    credits = pd.read_csv('tmdb_5000_credits.csv')
except FileNotFoundError:
    # Fallback if running from parent dir
    movies = pd.read_csv('movie-recommender/tmdb_5000_movies.csv')
    credits = pd.read_csv('movie-recommender/tmdb_5000_credits.csv')

# Merge on movie_id
# movies.csv has 'id', credits.csv has 'movie_id'
movies = movies.rename(columns={'id': 'movie_id'})
movies = movies.merge(credits, on='movie_id')

# Keep relevant columns
# Note: 'title_x' comes from movies, 'title_y' from credits.
# We'll use 'title_x' as title.
if 'title_x' in movies.columns:
    movies = movies.rename(columns={'title_x': 'title'})

# Handle Preprocessing
def convert(obj):
    L = []
    try:
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L
    except:
        return []

def convert3(obj):
    L = []
    counter = 0
    try:
        for i in ast.literal_eval(obj):
            if counter != 3:
                L.append(i['name'])
                counter += 1
            else:
                break
        return L
    except:
        return []

def fetch_director(obj):
    L = []
    try:
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
        return L
    except:
        return []

# Apply conversions
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)

# Collapse spaces
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

# Create soup
movies['overview'] = movies['overview'].fillna('')
movies['overview'] = movies['overview'].apply(lambda x: x.split())

def create_soup(x):
    # Joining all as space-separated string
    # "genres + keywords + cast + crew" (and user prompt implied these 4, but usually overview is used too.
    # checking strict user requirement: "genres + keywords + cast + crew"
    # User did NOT mention overview in 'soup'.
    # "Create a 'soup' feature using: genres + keywords + cast + crew"
    # I will stick to what they asked.
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + ' '.join(x['crew']) + ' ' + ' '.join(x['genres'])

movies['soup'] = movies.apply(create_soup, axis=1)

# Vectorization
cv = CountVectorizer(max_features=10000, stop_words='english')
vectors = cv.fit_transform(movies['soup']).toarray()

# Similarity
cosine_sim = cosine_similarity(vectors)

# Indices mapping
movies_df = movies[['movie_id', 'title', 'soup']].copy()
indices = pd.Series(movies_df.index, index=movies_df['title'])

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    return None



def recommend(movie_title: str) -> list:
    try:
        idx = indices[movie_title]
        if isinstance(idx, pd.Series):
             idx = idx.iloc[0]
             
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        
        movie_indices = [i[0] for i in sim_scores]
        
        # Return list of tuples (title, poster_url)
        results = []
        for i in movie_indices:
            movie_id = movies_df.iloc[i].movie_id
            title = movies_df.iloc[i].title
            poster = fetch_poster(movie_id)
            results.append((title, poster))
            
        return results
    except KeyError:
        return []

# List of titles for the dropdown
titles = movies_df['title'].values
