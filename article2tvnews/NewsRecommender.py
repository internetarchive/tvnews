# News Recommender version 2
# written by Max Reinisch

# Given a URL for a news article, recommend TV news
# clips similar to article contents

####################
##### IMPORTS ######
####################

import requests #TODO: use urllib3 instead of Requests
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine


####################
#### VARIABLES #####
####################

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
CALAIS_ENDPOINT = 'https://api.thomsonreuters.com/permid/calais'
CALAIS_TOKEN = "cvTFhY53VXBYm5HO85weHPx346W05015"
CALAIS_HEADER = {'X-AG-Access-Token' : CALAIS_TOKEN, 'Content-Type' : 'text/raw', 'outputformat' : 'application/json'}



def makeRecommendations(article):
    calais_json = getOpenCalaisResponse(article)
    entities = getSearchQuery(calais_json)
    GDELT_response = getDGELTv2Response(entities) #GDELT_response in JSON format
    if(GDELT_response.get('clips')):
        return list(sortClipsBySimilarity(GDELT_response.get("clips"), article))
    else:
        return []


def getOpenCalaisResponse(article):
    response = requests.post(CALAIS_ENDPOINT, data=article.get("body").encode('utf-8'), headers=CALAIS_HEADER, timeout=80)
    print("OpenCalais status code:", response.status_code)
    content = response.text

    c = json.loads(content)
    return c

def getSearchQuery(c):
    # This function is an unsolved problem.  How to find the best search query
    # Currently returns a list of all entities' names in order of number of mentions
    entities = [values for values in c.values() if values.get("_typeGroup") == "entities"]
    return [e.get('lastname') or e['name'] for e in sorted(entities, key=lambda x: len(x['instances']), reverse=True)]

def getDGELTv2Response(entities):
    good_result = False
    entities = entities[:3]
    while(not good_result):
        if len(entities) ==0:
            return {}
        query = " ".join([f'"{entity}"' for entity in entities])
        url = 'https://api.gdeltproject.org/api/v2/tv/tv?query='+query+ '%20market:%22National%22&mode=clipgallery&format=json&datanorm=perc&timelinesmooth=0&datacomb=sep&last24=yes&timezoom=yes&TIMESPAN=14days#'
        res = requests.get(url)
        # with open('log.txt', 'a') as f: # Log for Debugging purposes
        #     f.write(url)
        #     f.write(f'\nStatus Code: {res.status_code}\n')
        #     for entity in entities:
        #         f.write(entity + "-")
        #     f.write('\n')
        #     f.write(res.text)
        #     f.write('\n\n\n')
        gdelt_json = json.loads(res.text)
        if len(gdelt_json.keys()) ==0:
            entities = entities[0:-1]
        else:
            good_result = True
            print("search query:",query)
            print("GDELT status code:", res.status_code)
    return gdelt_json


def sortClipsBySimilarity(clips, article):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2) )
    bow = vectorizer.fit_transform([clip.get('snippet') for clip in clips])
    article_bow = vectorizer.transform([article.get('body')])
    cosine_distances = [cosine(vec.todense(), article_bow.todense()) for vec in bow]
    return zip(clips, cosine_distances)
