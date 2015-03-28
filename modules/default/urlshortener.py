# -*- coding: utf-8 -*-
import configs.module
import requests
import urllib.parse


def init():
    m = configs.module.Module('urlshortener')
    m.set_help('Use http://v.gd to shorten URLs.')
    m.add_command_hook('urlshorten',
        {
            'help': 'Shorten a URL.',
            'function': urlshorten,
            'args': [
                {
                    'name': 'url',
                    'help': 'URL to shorten.',
                    'optional': False,
                    },
                {
                    'name': 'ending',
                    'help': 'Custom ending.',
                    'optional': True,
                    },
                ]
            }
        )
    m.add_command_alias("short", "urlshorten")
    m.add_command_alias("shorten", "urlshorten")
    m.add_command_alias("vgd", "urlshorten")
    return m


def urlshorten(fp, args):
    return(requests.get(
        "http://v.gd/create.php", params={
        'format': 'simple',
        'url': (args.getlinstr('url')),
        'shorturl': (args.getlinstr('ending', ''))
        }
        ).text)