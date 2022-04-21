from dataclasses import replace
import pandas as pd
import sqlite3

def generateMovieDB():
    movies = pd.read_csv("dataset/movie.csv")
    movies["genres"] = movies["genres"].str.replace("|", ", ", regex=True)
    ratings =  pd.read_csv("dataset/rating.csv")
    #print(movies.head())
    #print(ratings.head())

    #Remove Users who have rated leass than 25 Ratings
    ratings = ratings.drop(["userId"], axis=1)
    ratingsFiltered = ratings.groupby(["movieId"]).mean()
    Movies = pd.merge(movies, ratingsFiltered, on="movieId", how="left")
    #Movies = Movies[["movieID","title","genres","rating"]]
    #print(Movies.head())
    movieDB = pd.DataFrame(Movies)
    conn = sqlite3.connect('database.db')
    '''
    create_query = "CREATE TABLE IF NOT EXISTS movies (movieID INTEGER, title TEXT, genres TEXT, rating REAL)"
    cursor = conn.cursor()
    cursor.execute(create_query)
    for row in Movies.itertuples:
        insert_query = "INSERT INTO movies (movieID, title, genres, rating) VALUES ({row[1]},'{row[2]}','{row[2]}',{row[4]})"
        cursor.execute(insert_query)'''
    movieDB.to_sql(name='movies', con=conn, if_exists="replace")