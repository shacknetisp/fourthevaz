# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('echo')
    m.set_help('Echo text and provide various text functions.')
    m.add_command_hook('echo',
        {
            'function': echo,
            'help': 'Echo text.',
            'noshlex': True,
            'args': [
                {
                    'name': 'text',
                    'optional': False,
                    'help': 'Text to echo.',
                    'end': True,
                    },
                {
                    'name': 'before',
                    'optional': True,
                    'help': 'Text to echo.',
                    'keyvalue': 'string',
                    },
                {
                    'name': 'after',
                    'optional': True,
                    'help': 'Text to echo.',
                    'keyvalue': 'string',
                    },
                ],
            })
    m.add_command_hook('bold',
        {
            'function': bold,
            'help': 'Echo bold text.',
            'noshlex': True,
            'args': [
                {
                    'name': 'text',
                    'optional': False,
                    'help': 'Text to echo bolded.',
                    'end': True,
                    },
                ],
            })
    return m


def echo(fp, args):
    return "%s%s%s" % (args.getlinstr('before', ''),
        args.getlinstr('text', ''),
        args.getlinstr('after', ''))


def bold(fp, args):
    return "\2%s\2" % args.getlinstr('text', '')