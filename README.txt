=================
Article 2 TV News
=================

Article2TVNews allows users to find TV news clips on subjects related
to an article they are reading.  It provides methods to extract text from an
article and get tv news clips based on the article's subject.  This package is
written for the Internet Archive's WayBack Machine and its Context browser
extension. Typical usage looks something like this::

    #!/usr/bin/env python

    from article2tvnews import ArticleExtraction, NewsRecommender

    url = "https://www.huffingtonpost.com/entry/alex-jones-infowars-app-apple-google_us_5b694ec3e4b0de86f4a4bc1d"
    html = ArticleExtraction.getHTML(url)
    article = ArticleExtraction.extract(html)
    for clip in NewsRecommender.makeRecommendations(article):
        print(clip)



Thanks
======

Thanks to the wonderful people at *The Internet Archive* for giving me this
opportunity, and a special thanks to:

* Mark

* Dvd

* Vangelis

* Anish

* And of course, Brewster Kahle
