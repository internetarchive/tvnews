from unittest import TestCase
from tvnews import ArticleExtraction, NewsRecommender

class TestNewsRecommender(TestCase):
    good_url = "https://www.huffingtonpost.com/entry/alex-jones-infowars-app-apple-google_us_5b694ec3e4b0de86f4a4bc1d"
    bad_url = "https://www.huffingtonpost.com/"
    def test_makeRecommendations_json_response(self):
        article = ArticleExtraction.extract(ArticleExtraction.getHTML(self.good_url))
        clips = NewsRecommender.makeRecommendations(article)
        for clip in clips:
            self.assertTrue(clip.get("preview_url"))
            self.assertTrue(clip.get("similarity"))
            self.assertTrue(clip.get("show"))

    def test_makeRecommendations_non_article(self):
        article = ArticleExtraction.extract(ArticleExtraction.getHTML(self.bad_url))
        clips = NewsRecommender.makeRecommendations(article)
        self.assertTrue(len(clips) == 0)

    def test_makeRecommendations_sort(self):
        article = ArticleExtraction.extract(ArticleExtraction.getHTML(self.good_url))
        clips = NewsRecommender.makeRecommendations(article)
        for i in range(len(clips)-1):
            self.assertTrue(clips[i].get("similarity") <= clips[i+1].get("similarity"))
