# -*- coding: utf-8 -*-
import configs.module
import importlib


def init():
    m = configs.module.Module('translate')
    m.set_help('Get translations.')
    m.add_command_hook('translate', {
        'function': translate,
        'help': 'Get translations.',
        'args': [
            {
                'name': 'from',
                'optional': True,
                'keyvalue': 'language',
                'help': 'Language to translate from. [Auto-Detect].',
                },
                    {
                'name': 'to',
                'optional': True,
                'keyvalue': 'language',
                'help': 'Language to translate to. [English].',
                },
            {
                'name': 'words',
                'optional': False,
                'help': 'Words to translate.',
                'end': True,
                },
            ]
        })
    return m


def getl(l):
    if l == 'auto':
        return l
    from . import iso639
    importlib.reload(iso639)
    item = iso639.find(whatever=l)
    if item:
        return item['iso639_1']
    raise ValueError("Cannot find '" + l + "'")


def translate(fp, args):
    from . import iso639
    importlib.reload(iso639)
    translate = fp.server.import_module('translate.translate', True)
    fromword = args.getlinstr('from', 'auto')
    toword = args.getlinstr('to', 'en')
    inp = args.getlinstr('words')
    try:
        r = translate.translate(inp, getl(fromword), getl(toword))
        fromword = r[1]
        try:
            fromword = iso639.find(whatever=fromword)['name']
        except ValueError:
            pass
        try:
            toword = iso639.find(whatever=toword)['name']
        except ValueError:
            pass
        return("%s to %s: %s" % (fromword, toword, r[0]))
    except ValueError as e:
        return(str(e))
