import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import operator

def filteringSuggestions(movieNames):
    contentFilteringLatentMatrix = pd.read_pickle("data/contentFiltering.pkl")
    collaborativeFilteringLatentMatrix = pd.read_pickle("data/collaborativeFiltering.pkl")
    movieDict = dict()
    for movie in movieNames:
        score = 0
        try:
            contentArray = np.array(contentFilteringLatentMatrix.loc[ movie ]).reshape(1,-1)
            contentScore = cosine_similarity(contentFilteringLatentMatrix, contentArray).reshape(-1)
            score += contentScore
        except:
            pass
        
        try:
            collaborativeArray = np.array(collaborativeFilteringLatentMatrix.loc[ movie ]).reshape(1,-1)
            collaborativeScore = cosine_similarity(collaborativeFilteringLatentMatrix, collaborativeArray).reshape(-1)
            if(score>0):
                score += collaborativeScore
                score /= 2
            else:
                score += collaborativeScore
        except:
            pass

        df = { "hybrid": score }
        similar = pd.DataFrame(df, index = contentFilteringLatentMatrix.index)
        similar.sort_values("hybrid", ascending=False, inplace=True)
        movieDict = movieDict | similar.head(50).to_dict()["hybrid"]
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
    # print(movieRecommendations)
    return movieRecommendations
