#!/usr/bin/python3.4
# Article Extraction Module
# written by Max Reinisch

# Given an article URL, extract the article body text

# TODO: use urllib3 instead of Requests

import json
import requests
import re
from readability import Document

header = {"Accept-Encoding": "gzip", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

def extract(html):
    """
    Simply uses regex and readability to get document body from html
    """

    doc = Document(html)
    json_ret = {"title": tag_re.sub('', doc.title()),
    "body": tag_re.sub('', doc.summary())}
    return json_ret

def getHTML(url):
    """
    Requests article and returns html
    """
    res = requests.get(url, headers=header)
    if res.status_code >=400:
        print("Requested URL returned status code: " + res.status_code)
        exit(-1)
    return res.text
