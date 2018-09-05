from unittest import TestCase
from tvnews import ArticleExtraction, NewsRecommender

class TestNewsRecommender(TestCase):
    url = "https://www.huffingtonpost.com/entry/alex-jones-infowars-app-apple-google_us_5b694ec3e4b0de86f4a4bc1d"

    def test_makeRecommendations_json_response(self):
        article = ArticleExtraction.extract(ArticleExtraction.getHTML(self.url))
        clips = NewsRecommender.makeRecommendations(article)
        for clip in clips:
            self.assertTrue(clip.get("preview_url"))
            self.assertTrue(clip.get("similarity"))
            self.assertTrue(clip.get("show"))
