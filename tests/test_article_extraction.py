import pytest
from tvnews import ArticleExtraction


GOOD_URL = "https://www.huffingtonpost.com/entry/alex-jones-infowars-app-apple-google_us_5b694ec3e4b0de86f4a4bc1d"
BAD_URL = "https://www.huffingtonpost.com/"


def test_getHTML():
    html = ArticleExtraction.getHTML(GOOD_URL)
    assert html


def test_extract_returns_dict():
    html = ArticleExtraction.getHTML(GOOD_URL)
    article = ArticleExtraction.extract(html)
    assert article
    assert article['title']
    assert article['body']
