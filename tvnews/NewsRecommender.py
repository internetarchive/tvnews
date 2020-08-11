# News Recommender version 2. Given a URL for a news article, recommend TV news
# clips similar to article contents
from collections import Counter
import logging
import json
import urllib3
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
import en_core_web_sm


CALAIS_ENDPOINT = 'https://api.thomsonreuters.com/permid/calais'
GDELT_HEADER = {'Content-Type': 'application/json',
                'outputformat': 'application/json'}
log = logging.getLogger(__name__)
urllib3.disable_warnings()
http = urllib3.PoolManager(num_pools=10, maxsize=10, cert_reqs='CERT_NONE')
nlp = en_core_web_sm.load()


def makeRecommendations(article, calais_token=False):
    query = getSearchQuery(article, calais_token)
    GDELT_response = getGDELTv2Response(query)  # GDELT_response in JSON format
    if GDELT_response.get('clips'):
        return list(sortClipsBySimilarity(GDELT_response.get("clips"), article))
    return []


def getSearchQuery(article, calais_token=False):
    if calais_token:
        calais_json = getOpenCalaisResponse(article, calais_token)
        if calais_json != "SpaCy":
            return parseCalais(calais_json)
    entities = extractEntities(article)
    return parseEntities(entities)


def extractEntities(article):
    """Get title twice to increase title weight.
    """
    doc = nlp(article["title"] + article["title"] + article["body"])
    return [x.text for x in doc.ents]


def parseEntities(entities):
    if len(entities) == 0:
        return []
    return [e[0] for e in Counter(entities).most_common(3)]


def getOpenCalaisResponse(article, calais_token):
    CALAIS_HEADER = {'X-AG-Access-Token': calais_token,
                     'Content-Type': 'text/raw',
                     'outputformat': 'application/json'}
    response = http.request('POST', CALAIS_ENDPOINT,
                            body=(article.get("title")+" "+article.get("body")).encode('utf-8'),
                            headers=CALAIS_HEADER, timeout=80)
    print(response)
    if response.status >= 400:
        log.warning("OpenCalais returned status code: %d. Falling back to SpaCy extraction protocol...", response.status)
        return "SpaCy"
    content = response.data.decode('utf-8')

    c = json.loads(content)
    return c


def parseCalais(c):
    # This function is an unsolved problem.  How to find the best search query
    # Currently returns a list of all entities' names in order of number of mentions
    entities = [values for values in c.values() if values.get("_typeGroup") == "entities"]
    if len(entities) == 0:
        return []
    return [e.get('lastname') or e['name'] for e in sorted(entities, key=lambda x: len(x['instances']), reverse=True)]


def getGDELTv2Response(query):
    entities = query[:3]
    while entities:
        query = "+".join(['"' + entity + '"' for entity in entities])
        res = http.request('GET', 'https://api.gdeltproject.org/api/v2/tv/tv',
                           fields={'query': query + ' market:"National"',
                                   'mode': 'clipgallery', 'format': 'json',
                                   'datanorm': 'perc', "timelinesmooth": 0,
                                   "datacomb": "sep", "last24": "yes",
                                   "timezoom": "yes", "TIMESPAN": "14days"})
        if res.status >= 400:
            log.error("GDELT returned status code: %d. Exiting...", res.status)
            return {}
        try:
            gdelt_json = json.loads(res.data.decode('utf-8'))
            if gdelt_json:
                return gdelt_json
        except ValueError:
            gdelt_json = {}

        entities.pop()
        log.info("GDELT returned 0 results. Simplifying search to: " + str(entities))

    log.warning("No search found. Returning empty result.")
    return {}


def sortClipsBySimilarity(clips, article):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    bow = vectorizer.fit_transform([clip.get('snippet') for clip in clips])
    article_bow = vectorizer.transform([article.get('body')])
    cosine_distances = [cosine(vec.todense(), article_bow.todense()) for vec in bow]
    ret = []
    for clip, dist in zip(clips, cosine_distances):
        clip.update({"similarity": dist})
        ret.append(clip)
    log.info(ret)
    return sorted(ret, key=lambda x: x.get('similarity'))
