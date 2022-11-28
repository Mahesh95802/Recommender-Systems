import pandas as pd
import json

def generateMovieList():
    try:
        movies = pd.read_csv("dataset/movie.csv")
    except:
        print("There was a problem in reading the datasets")
    movieList = [ movies["title"][i] for i in range(len(movies["title"])) ] 
    data = { "movies": movieList }
    # print(data)
    try:
        with open("data/movieList.json", "w") as f:
            json.dump(data, f)
    except:
        print("Error in creating MovieList JSON")
