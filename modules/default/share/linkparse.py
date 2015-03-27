# -*- coding: utf-8 -*-
import requests
from lxml.html import fromstring


def get_title(url):
    r = requests.get(url, timeout=1)
    tree = fromstring(r.content)
    return tree.findtext('.//title')