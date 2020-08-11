from tvnews import ArticleExtraction, NewsRecommender


GOOD_URL = "https://www.huffingtonpost.com/entry/alex-jones-infowars-app-apple-google_us_5b694ec3e4b0de86f4a4bc1d"
URLENCODE_URL = "https://www.vox.com/policy-and-politics/2018/9/24/17157194/rosenstein-trump-mueller-fired-doj-fbi"

EXPECTED_KEYS = ['preview_url', 'similarity', 'show', 'date', 'station',
                 'preview_thumb', 'snippet']


def test_makeRecommendations_json_response():
    article = ArticleExtraction.extract(ArticleExtraction.getHTML(GOOD_URL))
    clips = NewsRecommender.makeRecommendations(article)
    for clip in clips:
        for key in EXPECTED_KEYS:
            assert clip.get(key)


def test_makeRecommendations_using_urlencoding():
    article = ArticleExtraction.extract(ArticleExtraction.getHTML(URLENCODE_URL))
    clips = NewsRecommender.makeRecommendations(article)
    for clip in clips:
        for key in EXPECTED_KEYS:
            assert clip.get(key)


def test_makeRecommendations_sort():
    article = ArticleExtraction.extract(ArticleExtraction.getHTML(GOOD_URL))
    clips = NewsRecommender.makeRecommendations(article)
    for i in range(len(clips)-1):
        assert  clips[i].get("similarity") <= clips[i+1].get("similarity")


def test_makeRecommendations_bad_calais():
    article = ArticleExtraction.extract(ArticleExtraction.getHTML(GOOD_URL))
    clips = NewsRecommender.makeRecommendations(article, calais_token="klasdallksdlfaklke")
    for clip in clips:
        for key in EXPECTED_KEYS:
            assert clip.get(key)
