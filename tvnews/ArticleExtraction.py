# Article Extraction Module. Given an HTML doc, extract the article body text.
import re
from readability import Document


tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')


def extract(html):
    """Simply uses regex and readability to get document body from html
    """
    try:
        doc = Document(html)
        return {
            "title": tag_re.sub('', doc.title()),
            "body": tag_re.sub('', doc.summary())
                    .replace("\n", " ")
                    .replace("\xa0", " ")
                    .strip()
            }
    except Exception:
        # Note that readability-lxml as of 0.8.1 does not provide any custom
        # exceptions we could handle.
        return {}
