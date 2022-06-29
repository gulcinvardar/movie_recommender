# A Movie Recommender Web-App based on an NMF model, a user-similarity model, or a random selection

This project was written during Spiced Academy Data Science Bootcamp. 
It is one of the weekly projects.

This is a web-app using Flask. 

1. *Main page:*
<img src="https://github.com/gulcinvardar/movie_recommender/blob/main/example_images_of_pages/main_page.jpg" width="500" alt="Main Page">
The main page asks the user to select from:
- *Random recommendation* (I am feeling lucky)
- *NMF (Non-negative matrix factorization)* model (I want a good guess)
- *User-similarity* (What do people like me watch?)


2. *User-input page:*
<img src="https://github.com/gulcinvardar/movie_recommender/blob/main/example_images_of_pages/user_input_page.jpg" width="500" alt="Example User-Input page">
When selecting the method of the movie recommendation, the user is directed to the next page.
In the next page, the user should rate 5 movies and select the year and genre preference for the movie recommendation:
- Movie rating: The whole movie list is given as a selection list. 
The movies should be clicked from the list, but not written by the user
- Year preference: Before 2000, After 2000
- Genre preference: Is given as a list created from the genre documentation in the movie-info

3. *Movie recommendation page:*
<img src="https://github.com/gulcinvardar/movie_recommender/blob/main/example_images_of_pages/recommendation_page.jpg" width="500" alt="Example Recommendation page">
5 movies are recommended based on the recommendation method and the year and genre preference. 
If the user clicks on the recommended movie, they will be directed to the movie-info page on TMDB.


## Contents:

### Folders

- recommendation_movies:

Contains the csv files downloaded from [MovieLens](http://movielens.org)

- static:

Contains the images used in the web-app and the style.css file. 
The CSS file will be removed after the styling with Bootstrap is completed. 
For now, only the main page and the randomrecommendation pages are styled with Bootstrap, the rest will be done soon.

- templates:

Contains the HTML files. 
1. index.html : The main page. The user is asked to select from three recommendation methods.
2. random.html : The page the user is directed after selecting 'I am feeling lucky!'. 
The user should give the input for year and genre selection.
3. nmf.html : The page the user is directed after selecting 'I want a good guess!'. 
The user should rate 5 movies and give the input for year and genre selection.
4. user_sim.html : The page the user is directed after selecting 'What do people like me watch?'. 
The user should rate 5 movies and give the input for year and genre selection.
5. recommener_random.html, recommender_nmf.html, recommender_user.html : The pages where the recommended movies are shown.


### Files

- combine_csvs.py

Used for data preparation. 
The csvs that are in 'recommendation_movies' folder are combined to create a dataframe that includes the movie info for year, genre, and tmdb link.
The dataframe is saved as a csv file that is used to in utils.py. 
The genre and year info is implemented as user preference for movie recommendation.

- utils.py

Includes helper functions to be used in recommender.py and app.py. 
The functions are used to create user-dataframe, insert new user, sort year and genre, implement the tmdb link, and pickle the nmf model and factorizers.

- nmf_model.py

Non-negative matrix factorization

Creates the nmf model based on the user-ratings. 
For NA values simple imputer filling with constant average (2.5) is used. This can be changed for model optimization. 
The simple imputer is pickled as simpleimputer.pickle. Pickling of the imputation will be handy when different methods for imputation is used.
The rating matrix is pickled as R_table and R_imp_table. The Q factorizer is pickled as Q_table. The trained model is pickled as trained_nmf_model.

- recommender.py

Includes the three different methods used for movie recommendation

- app.py

Runs the web-app.

- Procfile and requirements.txt 
Files that are used to deploy the web-app to Heroku. 
For deployment please refer to [Heroku-Documentation](https://devcenter.heroku.com/categories/reference), especially [deployment-with-Git](https://devcenter.heroku.com/categories/deploying-with-git)

## Usage

To run the web-app locally: 
1. In your terminal go to the folder that includes all the files.
2. run the app.py

# Ideas for further development:

1. Play around with the imputation
2. Save the user and keep track of their rating 
3. Use IMDB API 