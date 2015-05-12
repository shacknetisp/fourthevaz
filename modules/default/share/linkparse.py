# -*- coding: utf-8 -*-
import requests
import utils


def get_title(url, timeout=1):
    r = requests.get(url, timeout=timeout)
    return utils.find_between(r.content.decode(), '<title>', '</title>')