#!/usr/bin/python3.4
# Article Extraction Module
# written by Max Reinisch

# Given an article URL, extract the article body text

import json
import urllib3
import re
from readability import Document


import logging

log = logging.getLogger(__name__)
header = {"Accept-Encoding": "gzip", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
urllib3.disable_warnings()
http = urllib3.PoolManager()
logging.getLogger('readability.readability').setLevel(logging.CRITICAL)

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
    res = http.request('GET', url, headers=header)
    if res.status >=400:
        log.error("Requested URL returned status code: " +str(res.status)+ ".  Exiting...")
        exit(1)
    # log.info(res.data)
    return res.data.decode('utf-8')
