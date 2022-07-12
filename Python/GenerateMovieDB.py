from dataclasses import replace
import pandas as pd
import sqlite3

def generateMovieDB():
    movies = pd.read_csv("dataset/movie.csv")
    movies["genres"] = movies["genres"].str.replace("|", ", ", regex=True)
    ratings =  pd.read_csv("dataset/rating.csv")
    #Remove Users who have rated leass than 25 Ratings
    ratings = ratings.drop(["userId"], axis=1)
    ratingsFiltered = ratings.groupby(["movieId"]).mean()
    Movies = pd.merge(movies, ratingsFiltered, on="movieId", how="left")
    #Movies = Movies[["movieID","title","genres","rating"]]
    #print(Movies.head())
    movieDB = pd.DataFrame(Movies)
    conn = sqlite3.connect('data/database.db')
    movieDB.to_sql(name='movies', con=conn, if_exists="replace")
