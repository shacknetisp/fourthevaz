# -*- coding: utf-8 -*-
import configs.module
import configs.mload


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
                'help': 'Language to translate from [Auto-Detect].',
                },
                    {
                'name': 'to',
                'optional': True,
                'keyvalue': 'language',
                'help': 'Language to translate to [English].',
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
    iso639 = configs.mload.import_module_py("translate.iso639", "default")
    item = iso639.find(whatever=l)
    if item:
        return item['iso639_1']
    raise ValueError("Cannot find '" + l + "'")


def translate(fp, args):
    gtapi = configs.mload.import_module_py("translate.translate", "default")
    fromword = args.getlinstr('from', '')
    toword = args.getlinstr('to', 'en')
    inp = args.getlinstr('words')
    translator = gtapi.TranslateService()
    if fromword == '':
        fromword = list(translator.detect(inp).keys())[0]
    try:
        return(translator.trans_sentence(
        getl(fromword), getl(toword), inp))
    except ValueError as e:
        return(str(e))
