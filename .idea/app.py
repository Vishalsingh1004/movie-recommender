import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = "3f5bf672a9c8a3cf5d8dc87e3aeaa56f"

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background-color: #141414;
            color: white;
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 14px;
        }
        .title {
            font-size: 48px;
            font-weight: bold;
            color: #E50914;
            text-align: center;
            margin-bottom: 30px;
        }
        .movie-card {
            background-color: #1f1f1f;
            border-radius: 12px;
            padding: 10px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            transition: transform 0.3s ease;
        }
        .movie-card:hover {
            transform: scale(1.05);
        }
        .movie-title {
            color: #fff;
            margin-top: 10px;
            font-size: 16px;
            font-weight: 600;
        }
        .stSelectbox label {
            color: #fff !important;
            font-size: 16px;
            font-weight: 500;
        }
        .stButton button {
            background-color: #E50914;
            color: white;
            font-weight: bold;
            padding: 0.5em 1.5em;
            border-radius: 6px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie_title):
    idx = movies[movies['title'] == movie_title].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown('<div class="title">🎬 Movie Recommender System</div>', unsafe_allow_html=True)

selected_movie_name = st.selectbox('Choose a movie to get recommendations:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{posters[i]}" width="100%" style="border-radius: 10px;">
                    <div class="movie-title">{names[i]}</div>
                </div>
            """, unsafe_allow_html=True)
