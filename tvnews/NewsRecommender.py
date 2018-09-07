#!/usr/bin/python3.4
# News Recommender version 2
# written by Max Reinisch

# Given a URL for a news article, recommend TV news
# clips similar to article contents

####################
##### IMPORTS ######
####################

import urllib3
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
import logging



####################
#### VARIABLES #####
####################

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
CALAIS_ENDPOINT = 'https://api.thomsonreuters.com/permid/calais'
CALAIS_TOKEN = "cvTFhY53VXBYm5HO85weHPx346W05015"
CALAIS_HEADER = {'X-AG-Access-Token' : CALAIS_TOKEN, 'Content-Type' : 'text/raw', 'outputformat' : 'application/json'}
log = logging.getLogger(__name__)
urllib3.disable_warnings()
http = urllib3.PoolManager()

def makeRecommendations(article):
    calais_json = getOpenCalaisResponse(article)
    entities = getSearchQuery(calais_json)
    GDELT_response = getGDELTv2Response(entities) #GDELT_response in JSON format
    if(GDELT_response.get('clips')):
        return list(sortClipsBySimilarity(GDELT_response.get("clips"), article))
    else:
        return []


def getOpenCalaisResponse(article):
    response = http.request('POST', CALAIS_ENDPOINT, body= article.get("body").encode('utf-8'), headers=CALAIS_HEADER, timeout=80)
    if response.status >= 400:
        log.error("OpenCalais returned status code: " + str(res.status) + ".  Exiting...")
        exit(-1)
    content = response.data.decode('utf-8')

    c = json.loads(content)
    return c

def getSearchQuery(c):
    # This function is an unsolved problem.  How to find the best search query
    # Currently returns a list of all entities' names in order of number of mentions
    entities = [values for values in c.values() if values.get("_typeGroup") == "entities"]
    return [e.get('lastname') or e['name'] for e in sorted(entities, key=lambda x: len(x['instances']), reverse=True)]

def getGDELTv2Response(entities):
    good_result = False
    entities = entities[:3]
    while(not good_result):
        if len(entities) ==0:
            log.warning("No search found.  Returning empty result.")
            return {}
        query = "+".join(['"' + entity + '"' for entity in entities])
        url = 'https://api.gdeltproject.org/api/v2/tv/tv?query='+query+ '%20market:%22National%22&mode=clipgallery&format=json&datanorm=perc&timelinesmooth=0&datacomb=sep&last24=yes&timezoom=yes&TIMESPAN=14days#'
        res = http.request('GET', url)


        if(res.status>=400):
            log.error("GDELT returned status code: " + str(res.status)+ ".  Exiting...")
            exit(-1)
        try:
            gdelt_json = json.loads(res.data.decode('utf-8'))
        except ValueError:
            log.warning("Bad GDELT response, Returning empty result.");
            return {}
        log.info(url)
        if len(gdelt_json.keys()) ==0:
            entities = entities[0:-1]
            log.info("GDLET returned 0 results. Simplifying search to: " + str(entities))
        else:
            good_result = True
    return gdelt_json


def sortClipsBySimilarity(clips, article):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2) )
    bow = vectorizer.fit_transform([clip.get('snippet') for clip in clips])
    article_bow = vectorizer.transform([article.get('body')])
    cosine_distances = [cosine(vec.todense(), article_bow.todense()) for vec in bow]

    for clip, dist in zip(clips, cosine_distances):
        clip.update({"similarity": dist})
    return clips
