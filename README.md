# Movie Recommender System

A content-based Movie Recommender System where users can enter their favorite movie and get top matching recommendations. This project leverages Python libraries such as Pandas, scikit-learn, and Streamlit, and is based on TF-IDF and Cosine Similarity.

## Features

- 4800+ movies dataset (TMDB, movies.csv)
- User-friendly Streamlit Web App interface
- Content-based recommendation using genres, keywords, tagline, cast, and director
- Cosine Similarity algorithm for recommendations
- Proper handling of null values and robust data preprocessing
- Fast movie search with fuzzy title matching (difflib)

## Dataset & Preprocessing

- Dataset: movies.csv (TMDB movies metadata)
- Features used: `genres`, `keywords`, `tagline`, `cast`, `director`
- Null values are replaced with blank strings
- TF-IDF Vectorizer is used to build the final feature matrix

## How It Works

1. Combine all relevant features into a single metadata string per movie
2. Generate feature vectors using TfidfVectorizer
3. Compute movie-to-movie similarities using Cosine Similarity
4. User inputs any movie title (supports fuzzy matching for typos)
5. The app suggests the top 10 most similar movies based on the input

## Project Structure
├── Movie_Recommendation_System.ipynb
├── movies.csv
└── app.py

## Usage
- streamlit run app.py


