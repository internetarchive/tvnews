from unittest import TestCase
from tvnews import ArticleExtraction

class TestArticleExtraction(TestCase):
    url = "https://www.huffingtonpost.com/entry/alex-jones-infowars-app-apple-google_us_5b694ec3e4b0de86f4a4bc1d"

    def test_getHTML_returns_string(self):
        html = ArticleExtraction.getHTML(self.url)
        self.assertTrue(isinstance(html, str))

    # def test_getHTML_handles_404(self):
    #     bad_url = "https://www.huffingtonpost.com/entry/alex-jones-infowars-app-apple-google_us_5b694ec3e4b0de86f4a4bc1e"
    #     # with self.assertRaises(HTTPError):
    #     try:
    #         html = ArticleExtraction.getHTML(bad_url)
    #     except urllib2.HTTPError:
    #

    def test_extract_returns_dict(self):
        html = ArticleExtraction.getHTML(self.url)
        article = ArticleExtraction.extract(html)
        self.assertTrue(isinstance(article, dict))
