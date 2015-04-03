# -*- coding: utf-8 -*-
import configs.module
import requests


def init():
    m = configs.module.Module(__name__)
    m.set_help('Use the fortune program.')
    m.add_command_hook('fortune',
        {
            'function': fortune,
            'help': 'Use the fortune program.',
            'args': [],
            })
    return m


def fortune(fp, args):
    json = requests.get("http://ghostclanre.tk/cgi-bin/fortune.py?n=100").json()
    if 'error' in json:
        return 'Error: %s.' % json['error']
    return json['fortune']