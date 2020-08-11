from tvnews import ArticleExtraction


def test_extract():
    good_html = """
<html>
    <head><title>test</title></head>
    <body>
        <p>This is a unit test</p>
    </body>
</html>"""
    bad_html = """"""

    article = ArticleExtraction.extract(good_html)
    assert article
    assert article['title']
    assert article['body']

    article = ArticleExtraction.extract(bad_html)
    assert article == {}
