from tvnews import ArticleExtraction, NewsRecommender
import urllib3


GOOD_URL = "https://www.huffingtonpost.com/entry/alex-jones-infowars-app-apple-google_us_5b694ec3e4b0de86f4a4bc1d"
URLENCODE_URL = "https://www.vox.com/policy-and-politics/2018/9/24/17157194/rosenstein-trump-mueller-fired-doj-fbi"

EXPECTED_KEYS = ['preview_url', 'similarity', 'show', 'date', 'station',
                 'preview_thumb', 'snippet']

http = urllib3.PoolManager(cert_reqs='CERT_NONE')
res = http.request('GET', GOOD_URL)
good_html = res.data.decode('utf-8')
res = http.request('GET', URLENCODE_URL)
urlencode_good_html = res.data.decode('utf-8')


def test_makeRecommendations_json_response():
    article = ArticleExtraction.extract(good_html)
    clips = NewsRecommender.makeRecommendations(article)
    for clip in clips:
        for key in EXPECTED_KEYS:
            assert clip.get(key)


def test_makeRecommendations_using_urlencoding():
    article = ArticleExtraction.extract(urlencode_good_html)
    clips = NewsRecommender.makeRecommendations(article)
    for clip in clips:
        for key in EXPECTED_KEYS:
            assert clip.get(key)


def test_makeRecommendations_sort():
    article = ArticleExtraction.extract(good_html)
    clips = NewsRecommender.makeRecommendations(article)
    for i in range(len(clips)-1):
        assert clips[i].get("similarity") <= clips[i+1].get("similarity")


def test_makeRecommendations_bad_calais():
    article = ArticleExtraction.extract(good_html)
    clips = NewsRecommender.makeRecommendations(article)
    for clip in clips:
        for key in EXPECTED_KEYS:
            assert clip.get(key)


def test_sortClipsBySimilarity():
    article = ArticleExtraction.extract(good_html)
    query = NewsRecommender.getSearchQuery(article)
    GDELT_response = NewsRecommender.getGDELTv2Response(query)
    sorted_clips = NewsRecommender.sortClipsBySimilarity(GDELT_response.get("clips"), article)
    for clip in sorted_clips:
        for key in EXPECTED_KEYS:
            assert clip.get(key)
    for i in range(len(sorted_clips)-1):
        assert sorted_clips[i].get("similarity") <= sorted_clips[i+1].get("similarity")
