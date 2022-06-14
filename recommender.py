"""
Contains various recommondation implementations
all algorithms return a list of movieids
"""

import pandas as pd
import numpy as np
from utils import insert_new_user, sort_year_genre, read_pickle, movie_tmdb_dict, movies
import pickle
from sklearn.metrics.pairwise import cosine_similarity


def recommend_random(year, genre, k=5):
    """
    Returns k random movies for user based on their genre and year selection.
    """
    if year == ['before 2000']:
        year = movies[movies['movie_year']<2000].set_index('title')
    else:
        year = movies[movies['movie_year']>=2000].set_index('title')
    genre_year = year[year[genre]==1]
    selected_movies = genre_year.index
    random_movies = np.random.choice(selected_movies, size=k)
    recommendation = movie_tmdb_dict(movies, random_movies)
    
    return recommendation 

    
def recommend_nmf(user_rating, year, genre, k=5):
    """
    Predicts based on NMF.
    Uses pickled imputer, NMF model, and vectorizer.
    """
    new_user, active_user, R = insert_new_user(user_rating)

    imputer = read_pickle("simpleimputer.pickle")
    model = read_pickle("trained_nmf_model.pickle")
    Q = read_pickle("Q_table.pickle")

    user_clean = imputer.transform(new_user)
    user_P = model.transform(user_clean)
    user_R = np.dot(user_P,Q)
    
    user_pred = pd.DataFrame({'user_input':new_user.values[0], 'predicted_ratings':user_R[0]}, index = R.columns)
    sorted = sort_year_genre(user_pred, year, genre, k)
    recommendation = movie_tmdb_dict(movies, sorted)

    return recommendation


def recommend_on_similarity(user_rating, genre, year, k=5, similar_users=5):
    """
    Recommends new movies based on user similarity.
    """
    predicted_ratings_movies = []
    new_user, active_user, R = insert_new_user(user_rating)

    R_null = pd.concat([R, new_user]).fillna(value = 0)
    R_t = R_null.T
    unseen_movies=list(R_t.index[R_t[active_user] == 0])

    cos_sim_table = pd.DataFrame(cosine_similarity(R_null), index=R_null.index, columns=R_null.index)
    cos_sim_table[active_user].sort_values(ascending=False)
    similar_user_list = list(cos_sim_table[active_user].sort_values(ascending=False).index[1:1 + similar_users])

    for movie in unseen_movies[:5000]:
        people_who_have_seen_the_movie = list(R_t.columns[R_t.loc[movie] > 0])
        num = 0
        den = 0
        try:
            for user in similar_user_list:
                if user in people_who_have_seen_the_movie:
                    rating = R_t.loc[movie, user]
                    similarity = cos_sim_table.loc[active_user, user]
                    num = num + rating * similarity
                    den = den + similarity
                    predicted_ratings = num/den
                    predicted_ratings_movies.append([predicted_ratings, movie])
        except ZeroDivisionError: 
            pass

    df_pred=pd.DataFrame(predicted_ratings_movies, columns=['predicted_ratings', 'title'])
    prediction = sort_year_genre(df_pred, year, genre, k)
    recommendation = movie_tmdb_dict(movies, prediction)

    return recommendation


