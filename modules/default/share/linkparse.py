# -*- coding: utf-8 -*-
import requests
from lxml.html import fromstring


def get_title(url, timeout=1):
    r = requests.get(url, timeout=timeout)
    tree = fromstring(r.content)
    return tree.findtext('.//title')