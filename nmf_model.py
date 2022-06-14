
import numpy as np
import pandas as pd
import pickle
from sklearn.impute import SimpleImputer
from sklearn.decomposition import NMF


def create_df():
    """
    Gets the ratings and the movie files 
    downloaded from https://grouplens.org/datasets/movielens/ (100K)
    """
    df_rat = pd.read_csv("recommendation_movies/ml-latest-small/ratings.csv")
    df_mov = pd.read_csv("recommendation_movies/ml-latest-small/movies.csv")
    df_merge = df_rat.merge(df_mov, how='left', on='movieId')
    df_merge = df_merge.set_index('userId')

    return df_merge
    

def create_r_table(df):
    """
    Creates the pivoted table (R_table) for NMF.
    Uses Simple Imputer for filling missing values.
    """
    R = pd.pivot_table(df, index=['userId'], columns=['title'], values='rating')
    most_rated = R.isna().sum().sort_values().nsmallest(100)
    imputer = SimpleImputer(strategy = 'constant', fill_value= 2.5)
    R_imp = imputer.fit_transform(R)
    pickle.dump(R, open('R_table.pickle', 'wb'))
    pickle.dump(R_imp, open('R_imp_table.pickle', 'wb'))
    pickle.dump(imputer, open('simpleimputer.pickle', 'wb'))

    return R, R_imp, most_rated, imputer


def get_q_p_values(model, R, R_imp):
    """
    Trains the NMF model and retrievesthe Q_table"""
    model.fit(R_imp)
    Q = model.components_
    Q_df = pd.DataFrame(Q, columns=R.columns, index=features)
    P = model.transform(R_imp)
    P_df = pd.DataFrame(P, columns=features, index=R.index)
    pickle.dump(model, open('trained_nmf_model.pickle', 'wb'))
    pickle.dump(Q, open('Q_table.pickle', 'wb'))

    return Q_df, P_df, Q


def model_and_features(x, n):
    """
    To select the number of model components and iteration. 
    Retrieves the column names according to the number of model components."""
    model = NMF(n_components=x, max_iter= n) 
    features =[]
    for i in range(x):
        features.append(f'feature{i+1}')

    return model, features
    

if __name__ is '__main__':
    df = create_df()
    R, R_imp, most_rated, imputer = create_r_table(df)
    model, features = model_and_features(300, 500)
    Q_df, P_df, Q = get_q_p_values(model, R, R_imp)
