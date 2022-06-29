# A Movie Recommender Web-App based on an NMF model, a user-similarity model, or a random selection

This project was written during Spiced Academy Data Science Bootcamp. 
It is one of the weekly projects.

This is a web-app using Flask. 
1. Main page:
The main page asks the user to select from:
- Random recommendation (I am feeling lucky)
- NMF model (I want a good guess)
- User-similarity (What do people like me watch?)

2. User-input page:
When selecting the method of the movie recommendation, the user is directed to the next page.
In the next page, the user should rate 5 movies and select the year and genre preference for the movie recommendation:
- Movie rating: The whole movie list is given as a selection list. 
The movies should be clicked from the list, but not written by the user
- Year preference: Before 2000, After 2000
- Genre preference: Is given as a list created from the genre documentation in the movie-info

3. Movie recommendation:
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
4. recommener_random.html, recommender_nmf.html, recommender_user.html : The pages where the recommended movies are shown.





# Ideas for further development:

Save the user and keep track of their rating 
Use IMDB API 