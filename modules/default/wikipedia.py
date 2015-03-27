# -*- coding: utf-8 -*-
import configs.module
import wikipedia


def init():
    m = configs.module.Module('wikipedia')
    m.set_help('Get wikipedia definitions.')
    m.add_command_hook('wikipedia', {
        'function': wiki,
        'help': 'Get a definition from http://en.wikipedia.org/',
        'args': [
            {
                'name': 'page',
                'optional': False,
                'help': 'Page to look for.',
                'end': True,
                },
            ]
        })
    m.add_command_alias('w', 'wikipedia')
    m.add_command_alias('wiki', 'wikipedia')
    return m


def wiki(fp, args):
    out = "No definition found."
    try:
        one = str(wikipedia.summary(args.getlinstr('page'), sentences=1))
        two = str(wikipedia.summary(args.getlinstr('page'), sentences=2))
        if len(two) <= len(one) * 3:
            out = two
        out = one
    except wikipedia.exceptions.DisambiguationError as exc:
        one = wikipedia.summary(exc.options[0], sentences=1)
        two = wikipedia.summary(exc.options[0], sentences=2)
        if len(two) <= len(one) * 3:
            out = two
        out = one
    except wikipedia.exceptions.PageError:
        pass
    return out.replace('\n', '')



