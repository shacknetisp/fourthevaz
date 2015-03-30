# -*- coding: utf-8 -*-
import configs.module
import configs.locs
from . import wordai


def init(options):
    server = options['server']
    server.state['wordai'] = wordai.wordai(
        configs.locs.userdata + '/chatbot.%s.pkl' % server.entry['settings'])
    server.state['wordai'].load()
    m = configs.module.Module(__name__)
    m.set_help('Talk with the chatbot.')
    m.add_command_hook('chatbot',
        {
            'function': chatbot,
            'level': 1,
            'help': 'Talk to the bot.',
            'noshlex': True,
            'args': [
                {
                    'name': 'fix',
                    'help': 'Change the first word of arg to the second word.',
                    'keyvalue': '',
                    'optional': True,
                    },
                {
                    'name': 'count',
                    'help': 'Get the word count.',
                    'keyvalue': '',
                    'optional': True,
                    },
                {
                    'name': 'args',
                    'help': 'Arguments or message to send.',
                    'optional': False,
                    'end': True,
                    },
                ]
            })
    m.add_command_alias('c', 'chatbot')
    m.add_command_alias('talk', 'chatbot')
    return m


def chatbot(fp, args):
    wordai = fp.server.state['wordai']
    if 'count' in args.lin:
        return str(wordai.getwords())
    elif 'fix' in args.lin:
        try:
            f, t = args.getlinstr('args').split()
        except IndexError:
            return 'Usage: -fix <from> <to>.'
        wordai.replace(f, t)
        return '"%s" is now "%s".' % (f, t)
    else:
        return wordai.process(args.getlinstr('args'))