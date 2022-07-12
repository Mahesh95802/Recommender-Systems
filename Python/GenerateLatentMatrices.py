import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
#from Python.generateMovieList import generateMovieList

def generateLatentMatrices():
    #Read the Datasets
    try:
        movies = pd.read_csv("dataset/movie.csv")
        tags = pd.read_csv("dataset/tag.csv")
        ratings =  pd.read_csv("dataset/rating.csv")
    except:
        print("There was a problem in reading the datasets")
    
    #Check if the Data is read properly
    #print(movies.head())
    #print(ratings.head())
    #print(tags.head())

    movies["genres"] = movies["genres"].str.replace("|", " ", regex=True)

    #print(movies.head())
    #print(len(movies["movieId"].unique()))
    #print(len(ratings["movieId"].unique()))

    #Join tags and movie Dataset
    tagsAndMovies = pd.merge(movies, tags, on="movieId", how="left")
    #print(tagsAndMovies.head())

    #Merge the tags of the same movie into a single sentence
    tagsAndMovies.fillna("",inplace=True)
    tagsAndMovies = pd.DataFrame(tagsAndMovies.groupby("movieId")["tag"].apply(lambda x: "%s" % " ".join(x)))
    contentFiltering = pd.merge(movies, tagsAndMovies, on="movieId", how="left")
    #print(contentFiltering.head())

    #Combine Genres and Tags to create MetaData
    contentFiltering["MetaData"] = contentFiltering[["tag", "genres"]].apply(lambda x: " ".join(x), axis=1)
    #print(contentFiltering.head())

    #Convert the Metadata into a matrix
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(contentFiltering["MetaData"])
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index=contentFiltering.index.tolist())
    #print(tfidf_df.shape)

    #Finding Siginificant features with SVD
    noOfFeatures = 1000
    contentSVD = TruncatedSVD(n_components=noOfFeatures)
    contentLatentMatrix_AfterSVD = contentSVD.fit_transform(tfidf_df)

    '''
    #plot the variance
    explained = contentSVD.explained_variance_ratio_.cumsum()
    plt.plot(explained, ".-", ms=16, color="red")
    plt.show()
    '''
    
    #Dataframe Reduced to the requied dimensions
    contentLatentMatrix_AfterSVD = pd.DataFrame(contentLatentMatrix_AfterSVD[:,0:noOfFeatures], index=contentFiltering.title.tolist())
    #print(latentMatrix_AfterSVD.head())
    
    try:
        contentLatentMatrix_AfterSVD.to_pickle("data/contentFiltering.pkl")
        del contentLatentMatrix_AfterSVD
    except:
        print("There was a problem in Saving the Content Filtering Latent Matrix")

    print("ContentFiltering Latent Matrix generated")

    # ratingsFiltered = ratings.groupby("userId").filter(lambda x: len(x) >= 25 )
    # ratingsFiltered = pd.merge(movies["movieId"], ratingsFiltered, on="movieId", how="right")
    # ratingsFiltered = ratingsFiltered.pivot(index="movieId", columns="userId", values="rating").fillna(0)
    # #print(ratingsFiltered.head())

    # collaborativeSVD = TruncatedSVD(n_components=noOfFeatures)
    # collaborativeLatentMatrix_AfterSVD = collaborativeSVD.fit_transform(ratingsFiltered)
    # print("SVD 2 Done")

    # '''
    # #plot the variance
    # explained = collaborativeSVD.explained_variance_ratio_.cumsum()
    # plt.plot(explained, ".-", ms=16, color="red")
    # plt.show()
    # '''

    # collaborativeLatentMatrix_AfterSVD = pd.DataFrame(collaborativeLatentMatrix_AfterSVD, index=contentFiltering.title.tolist())
    # #print(collaborativeLatentMatrix_AfterSVD.head())
    
    # try:
    #     collaborativeLatentMatrix_AfterSVD.to_pickle("data/collaborativeFiltering.pkl")
    # except:
    #     print("There was a problem in Saving the Collaborative Filtering Latent Matrix")

    print("Latent Matrices Generated")


    