# -*- coding: utf-8 -*-
import requests


def getinfo(inp):
    response = requests.get(
            str('http://ip-api.com/json/%s' % inp)
        )
    ret = response.json()
    if not inp.strip() or ret['status'] != 'success':
        return None
    return ret