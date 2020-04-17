### Final Project - Prediction of popularity: explaining song popularity from Spotify data

This project has the objective of displaying the relationship between song data - audio features from the Spotify database - and song popularity measured by the number of streams a song has on Spotify.

From the Spotify database API, a 20,000 songs were analyzed from different genres.  

After using Python and some data wrangling techniques, we created data frame that was used to do some exploratory data analysis. Our Target Variable is Popularity and the Independent Variables are:
Acousticness, Danceability, Duration, Energy, Instrumentalness, Key, Liveness, Loudness, Mode, Speechiness, Tempo, Valence and
Followers.


Looking at the distributions of each feature, there is no clear correlation between the popularity of a songs, and other features.
The only features that show some correlation are loudness, acousticness and energy.

![Key Features & Correlation Matrix](Heat Map link-to-image-github)

We used classification algorithms to predict whether a song will be popular or not. We used historical data to train the  model and built a prediction model by regression. The 3 models we used are: Logistic Regression, Random Forest, k-Nearest Neighbor and Decision Tree.

![Model Performance](screenshot model_performance_accuracy and auc and  link-to-image-github)



We can conclude that our results suggest that audio features from Spotify have little to moderate impact in predicting song popularity.




More Info:  [Prezi Presentation](https://prezi.com/view/6GrxZQ6CnhMpSGklysZ1/)
