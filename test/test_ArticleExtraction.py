from unittest import TestCase
from tvnews import ArticleExtraction

class TestArticleExtraction(TestCase):
    good_url = "https://www.huffingtonpost.com/entry/alex-jones-infowars-app-apple-google_us_5b694ec3e4b0de86f4a4bc1d"
    def test_getHTML_returns_string(self):
        html = ArticleExtraction.getHTML(self.good_url)
        self.assertTrue(isinstance(html, str))



    def test_extract_returns_dict(self):
        html = ArticleExtraction.getHTML(self.good_url)
        article = ArticleExtraction.extract(html)
        self.assertTrue(isinstance(article, dict))
