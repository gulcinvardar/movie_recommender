import numpy as np
import pandas as pd
from pathlib import Path 

def combine_ratings_movies():
    """
    Gets the ratings and the movie files 
    downloaded from https://grouplens.org/datasets/movielens/ (100K)
    Cleans the movie name and extracts the year.
    """
    df_rat = pd.read_csv("recommendation_movies/ratings.csv")
    df_mov = pd.read_csv("recommendation_movies/movies.csv")
    df = df_rat.merge(df_mov, how='left', on='movieId')
    df['movie'] = df.title.str.split("(", expand = True)[0].str.strip("'").str.rstrip(" ").str.lstrip(" ").str.replace(", The", "")
    df['movie_year'] = df.title.str.split("(").str[-1].str.replace("[\D]", "")
    df['movie_year'] = df["movie_year"].replace({"": 0})
    df['movie_year'] = df["movie_year"].astype(int)
    df = df.set_index('userId')

    return df

def add_genre_links(df):
    """
    Puts the genres and the imdb links into the dataframe.
    """
    df_links = pd.read_csv("recommendation_movies/links.csv")
    df_all = df.merge(df_links, how='left', on='movieId')
    genres = df_all['genres'].str.get_dummies('|')
    df_dummy =  pd.concat([df_all, genres], axis=1)
    movie_infos = df_dummy.groupby('title').max().reset_index()
    filepath = Path("/Users/gulcinvardar/Desktop/Data_Science_Bootcamp/stationary-sriracha-student-code/projects/week_10/movie_recom")
    movie_infos.to_csv(f'{filepath}/movies_info.csv', sep = ',', index=True)

if __name__ is '__main__':
    df = combine_ratings_movies()
    add_genre_links(df)
