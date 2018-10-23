#!/usr/bin/python3.4
# News Recommender version 2
# written by Max Reinisch

# Given a URL for a news article, recommend TV news
# clips similar to article contents

####################
##### IMPORTS ######
####################

import urllib3
from urllib.parse import urlencode
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
import spacy
from collections import Counter
import en_core_web_sm
import logging



####################
#### VARIABLES #####
####################

GDELT_HEADER = {'Content-Type' : 'application/json', 'outputformat' : 'application/json'}
log = logging.getLogger(__name__)
urllib3.disable_warnings()
http = urllib3.PoolManager()
nlp = en_core_web_sm.load()


def makeRecommendations(article):
    # calais_json = getOpenCalaisResponse(article)
    entities = extractEntities(article)
    query = getSearchQuery(entities)
    GDELT_response = getGDELTv2Response(query) #GDELT_response in JSON format
    if(GDELT_response.get('clips')):
        return list(sortClipsBySimilarity(GDELT_response.get("clips"), article))
    return []

def extractEntities(article):
    doc = nlp(article["title"] + article["title"] + article["body"])
    return [x.text for x in doc.ents]

def getSearchQuery(entities):
    # This function is an unsolved problem.  How to find the best search query
    # Currently returns a list of all entities' names in order of number of mentions
    # entities = [values for values in c.values() if values.get("_typeGroup") == "entities"]
    if len(entities) == 0:
        return []

    return [e[0] for e in Counter(entities).most_common(3)]

def getGDELTv2Response(entities):
    good_result = False
    entities = entities[:3]
    while(not good_result):
        if len(entities) ==0:
            log.warning("No search found.  Returning empty result.")
            return {}
        query = "+".join(['"' + entity + '"' for entity in entities])
        encoded_args = urlencode({'query': query+' market:"National"', 'mode':'clipgallery', 'format':'json', 'datanorm':'perc',"timelinesmooth":0, "datacomb":"sep", "last24":"yes", "timezoom":"yes", "TIMESPAN":"14days"})
        url = 'https://api.gdeltproject.org/api/v2/tv/tv?' + encoded_args
        res = http.urlopen("GET", url)


        if(res.status>=400):
            log.error("GDELT returned status code: " + str(res.status)+ ".  Exiting...")
            return {}
        try:
            gdelt_json = json.loads(res.data.decode('utf-8'))
        except ValueError:
            log.warning("Bad GDELT response, Returning empty result.");
            log.warning(url)
            gdelt_json = {}
        # log.info(url)
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
    ret = []
    for clip, dist in zip(clips, cosine_distances):
        clip.update({"similarity": dist})
        ret.append(clip)
    # log.info(ret)
    return sorted(ret, key = lambda x: x.get('similarity'))
