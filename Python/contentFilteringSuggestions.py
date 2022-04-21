import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import operator

def contentFilteringSuggestions(movieNames):
    contentFilteringLatentMatrix = pd.read_pickle("contentFiltering.pkl")
    movieDict = dict()
    for movie in movieNames:
        a = np.array(contentFilteringLatentMatrix.loc[ movie ]).reshape(1,-1)
        score = cosine_similarity(contentFilteringLatentMatrix, a).reshape(-1)
        df = {"content":score}
        similar = pd.DataFrame(df, index = contentFilteringLatentMatrix.index)
        similar.sort_values("content", ascending=False, inplace=True)
        movieDict = movieDict | similar.head(50).to_dict()["content"]
        for m in movieNames:
            try:
                movieDict.pop(m)
                #print(m)
            except:
                pass
        movieDict = dict( sorted(movieDict.items(), key=operator.itemgetter(1),reverse=True))
        while(len(movieDict)>25):
            movieDict.popitem()
    movieRecommendations = pd.DataFrame({"title":movieDict.keys(), "propensity":movieDict.values()})
    #print(movieRecommendations)
    return movieRecommendations
