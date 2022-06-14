
import pandas as pd
import numpy as np
from fuzzywuzzy import process
import pickle

movies = pd.read_csv("movies_info.csv", index_col=0) 
genres = movies['genres'].str.split('|').explode().unique().tolist()
years = ['before 2000', 'after 2000']

def match_movie_title(input_title):
    """
    Matches inputed movie title to existing one in the list with fuzzywuzzy
    """
    movie_titles = movies['title']
    matched_title = process.extractOne(input_title, movie_titles)[0]

    return matched_title

def read_pickle(filename):
    """
    Reads pickled models and vectors.
    """
    with open(filename, "rb") as vectorizer:
        return pickle.load(vectorizer)
    

def create_user_dataframe(titles, ratings):
    """
    Converts the user input of movie ratings into a dictionary.
    """       
    ratings = map(int, ratings)
    user_rating = dict(zip(titles,ratings))
    return user_rating

def insert_new_user(user_rating):
    """
    Creates a dtaframe with the user input.
    """
    R = read_pickle("R_table.pickle")
    active_user ='new_user'
    user_input = pd.DataFrame(user_rating, index=[active_user])
    movies =pd.DataFrame(columns=R.columns)
    new_user = pd.concat([movies, user_input])

    return new_user, active_user, R

def sort_year_genre(df, year, genre, k):
    """
    Sorts the concatenated table of predicted ratings with the movie infos.
    Sorts based on user's selection of year and genre.
    """
    pred_with_movie_info = pd.merge(df, movies, on='title')
    pred_with_movie_info = pred_with_movie_info.sort_values([genre, 'predicted_ratings'], ascending=False)
    if year == ['before 2000']:
        prediction = pred_with_movie_info[pred_with_movie_info['movie_year']<2000].set_index('title')
        recommendation = prediction.head(k).index
    else:
        prediction = pred_with_movie_info[pred_with_movie_info['movie_year']>=2000].set_index('title')
        recommendation = prediction.head(k).index

    return recommendation

def movie_tmdb_dict(movies_df, recommended_movies):
    """
    Creates a dictionary of dictonaries with the title and the TMDB link of the recommended movie. 
    movies_df: movies_info table
    movies: recommended movies list.
    """
    tmdb_links = []
    for movie in recommended_movies:
        tmdb_id = int(movies_df[movies_df['title'] == movie]['tmdbId'])
        link = f'https://www.themoviedb.org/movie/{tmdb_id}/'
        tmdb_links.append(link)
    
    recommendation = map(dict, map(lambda t:zip(('title','link'),t), zip(recommended_movies,tmdb_links)))
    return recommendation

