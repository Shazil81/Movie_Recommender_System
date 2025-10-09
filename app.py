import streamlit as st
import pickle
import difflib
import requests
import time

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZmVlNjFmNzdkNmI5M2MxN2ZiMGY2ZGYyNDVkMzAxZSIsIm5iZiI6MTc1OTU2Mzg1Ni41NjgsInN1YiI6IjY4ZTBkMDUwOWMwNDUyZjg4ZjYxNmY0MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.xyHRCMIaC1wCZS8ozy0BF56_u9-YIzBO4v4GiycbhcE"


def fetch_poster(movie_id):
    """Fetch movie poster safely with retries (3 attempts)."""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    return "https://image.tmdb.org/t/p/w500/" + poster_path
                else:
                    return "https://via.placeholder.com/500x750?text=No+Poster"
        except requests.exceptions.RequestException:
            time.sleep(0.5)  # small delay before retry

    st.warning(f"⚠ Poster unavailable for movie ID {movie_id}.")
    return "https://via.placeholder.com/500x750?text=Poster+Unavailable"


def recommend(movie):
    """Recommend same + top 4 similar movies."""
    list_of_all_titles = movies_list['title'].tolist()
    find_close_match = difflib.get_close_matches(movie, list_of_all_titles)

    if not find_close_match:
        st.warning("No close match found for the selected movie.")
        return [], []

    close_match = find_close_match[0]
    index_of_the_movie = movies_list[movies_list.title == close_match]['index'].values[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommended_movies = []
    recommended_movies_poster = []
    count = 0

    # ✅ Now don't skip the same movie itself
    for index, score in sorted_similar_movies:
        movie_row = movies_list[movies_list.index == index]
        if movie_row.empty:
            continue

        movie_id = movie_row['id'].values[0]
        title_from_index = movie_row['title'].values[0]
        recommended_movies.append(title_from_index)
        recommended_movies_poster.append(fetch_poster(movie_id))

        count += 1
        if count == 5:  # show main + 4 similar
            break

    return recommended_movies, recommended_movies_poster


# Load model data
movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("🎬 Movie Recommender System")

Select_Movie_Name = st.selectbox('', movies_list['title'].tolist())

if st.button('Recommend'):
    names, posters = recommend(Select_Movie_Name)

    # Making 5 columns
    cols = st.columns(5)
    for i in range(min(5, len(names))):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])