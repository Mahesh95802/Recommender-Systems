import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import warnings

# warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

def generateLatentMatrices():
    # # Read the Datasets
    try:
        movies = pd.read_csv("dataset/movie.csv")
        tags = pd.read_csv("dataset/tag.csv")
        ratings =  pd.read_csv("dataset/rating.csv")
    except:
        print("There was a problem in reading the datasets")
    
    # # Check if the Data is read properly
    # print(movies.head())
    # print(ratings.head())
    # print(tags.head())

    movies["genres"] = movies["genres"].str.replace("|", " ", regex=True)

    # print(movies.head())
    # print(len(movies["movieId"].unique()))
    # print(len(ratings["movieId"].unique()))

    # # Join tags and movie Dataset
    tagsAndMovies = pd.merge(movies, tags, on="movieId", how="left")
    # print(tagsAndMovies.head())

    # # Merge the tags of the same movie into a single sentence
    tagsAndMovies.fillna("",inplace=True)
    tagsAndMovies = pd.DataFrame(tagsAndMovies.groupby("movieId")["tag"].apply(lambda x: "%s" % " ".join(x)))
    contentFiltering = pd.merge(movies, tagsAndMovies, on="movieId", how="left")
    #print(contentFiltering.head())

    # # Combine Genres and Tags to create MetaData
    contentFiltering["MetaData"] = contentFiltering[["tag", "genres"]].apply(lambda x: " ".join(x), axis=1)
    # print(contentFiltering.head())

    # # Convert the Metadata into a matrix
    # # tfdif - Term Frequency - Inverse Document Frequency
    tfidf = TfidfVectorizer(stop_words="english")
    tfidfMatrix = tfidf.fit_transform(contentFiltering["MetaData"])
    tfidfDataframe = pd.DataFrame(tfidfMatrix.toarray(), index=contentFiltering.index.tolist())
    # print(tfidfDataframe.shape)

    # # Finding Siginificant features with SVD
    noOfFeatures = 1000
    contentSVD = TruncatedSVD(n_components=noOfFeatures)
    contentLatentMatrixAfterSVD = contentSVD.fit_transform(tfidfDataframe)

    # # plot the variance
    # explained = contentSVD.explained_variance_ratio_.cumsum()
    # plt.plot(explained, ".-", ms=16, color="red")
    # plt.show()
    
    # # Dataframe Reduced to the requied dimensions
    contentLatentMatrixAfterSVD = pd.DataFrame(contentLatentMatrixAfterSVD[:,0:noOfFeatures], index=contentFiltering.title.tolist())
    # print(latentMatrix_AfterSVD.head())
    
    try:
        contentLatentMatrixAfterSVD.to_pickle("data/contentFiltering.pkl")
        del contentLatentMatrixAfterSVD
    except:
        print("There was a problem in Saving the Content Filtering Latent Matrix")

    print("ContentFiltering Latent Matrix generated")
    
    ratingsFiltered = pd.DataFrame(ratings.groupby("userId").filter(lambda x: len(x) >= 25 ))
    ratingsFiltered = pd.merge(movies["movieId"], ratingsFiltered, on="movieId", how="right")
    # print(ratingsFiltered.info())
    ratingsFiltered.pop("timestamp")
    ratingsFiltered["movieId"] = pd.to_numeric(ratingsFiltered["movieId"], downcast='integer')
    ratingsFiltered["userId"] = pd.to_numeric(ratingsFiltered["userId"], downcast='integer')
    ratingsFiltered["rating"] = pd.to_numeric(ratingsFiltered["rating"], downcast='float')
    # print(ratingsFiltered.info())
    ratingsFiltered = ratingsFiltered.pivot(index="movieId", columns="userId", values="rating").fillna(0)
    # print(ratingsFiltered.info())
    collaborativeSVD = TruncatedSVD(n_components=noOfFeatures)
    collaborativeLatentMatrixAfterSVD = collaborativeSVD.fit_transform(ratingsFiltered)

    # # plot the variance
    # explained = collaborativeSVD.explained_variance_ratio_.cumsum()
    # plt.plot(explained, ".-", ms=16, color="red")
    # plt.show()

    filteredMovieList = (pd.merge(movies, ratingsFiltered, on="movieId", how="right"))["title"].tolist()
    collaborativeLatentMatrixAfterSVD = pd.DataFrame(collaborativeLatentMatrixAfterSVD, index=filteredMovieList)
    # print(collaborativeLatentMatrixAfterSVD.head())
    
    try:
        collaborativeLatentMatrixAfterSVD.to_pickle("data/collaborativeFiltering.pkl")
    except:
        print("There was a problem in Saving the Collaborative Filtering Latent Matrix")

    print("ContentFiltering Latent Matrix generated")

    print("Latent Matrices Generated")


    