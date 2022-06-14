
from flask import Flask,render_template, request
from utils import create_user_dataframe, movies, genres, years
from recommender import recommend_nmf, recommend_on_similarity, recommend_random


app = Flask(__name__)

@app.route('/')
def welcome():
    """
    Route for welcome page.
    User can select 3 different recommendation methods.
    """
    return render_template('index.html')


@app.route('/random-recommend', methods=['GET', 'POST'])
def rand_recommend():
    """
    Recommends movies randomly.
    No user-input.
    """

    if request.method == 'GET':
        return render_template('random.html', genres=genres, years=years)
    year = request.form.getlist('year')
    genre = request.form.getlist('genre')[0]
    movie_ids = recommend_random(year, genre, k=5)

    return  render_template('recommender_random.html',movie_ids=movie_ids)

@app.route('/nmf-recommend', methods=['GET', 'POST'])
def nmf_recommend():
    """
    Recommends movies based on nmf model.
    Gets user-input as movie rating.
    """
    if request.method == 'GET':
        return render_template('nmf.html',
        movies=movies['title'].tolist(), genres=genres, years=years)
    titles = request.form.getlist('title')
    ratings = request.form.getlist('ratings')
    year = request.form.getlist('year')
    genre = request.form.getlist('genre')[0]
    user_rating = create_user_dataframe(titles, ratings)
    movie_ids = recommend_nmf(user_rating, year, genre, k=5)

    return  render_template('recommender_nmf.html', movie_ids=movie_ids)

@app.route('/user-recommend', methods=['GET', 'POST'])
def user_recommend():
    """
    Recommends movies based on user similarity.
    Gets user-input as movie rating.
    """
    if request.method == 'GET':
        return render_template('user_sim.html',
        movies=movies['title'].tolist(), genres=genres, years=years)
    titles = request.form.getlist('title')
    ratings = request.form.getlist('ratings')
    year = request.form.getlist('year')
    genre = request.form.getlist('genre')[0]
    user_rating = create_user_dataframe(titles, ratings)
    movie_ids = recommend_on_similarity(user_rating, genre, year, k=5, similar_users=5)

    return  render_template('recommender_user.html',movie_ids=movie_ids)


if __name__=='__main__':
    app.run(debug=True,port=5000)
