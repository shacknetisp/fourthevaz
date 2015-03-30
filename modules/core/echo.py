# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('echo')
    m.set_help('Echo text and provide various text functions.')
    m.add_command_hook('echo',
        {
            'function': echo,
            'help': 'Echo text.',
            'args': [
                {
                    'name': 'text',
                    'optional': False,
                    'help': 'Text to echo.',
                    'end': True,
                    },
                ],
            })
    m.add_command_hook('noquote',
        {
            'function': noquote,
            'noshlex': True,
            'help': 'Echo text without shlex processing.',
            'args': [
                {
                    'name': 'text',
                    'optional': False,
                    'help': 'Text to echo.',
                    'end': True,
                    },
                ],
            })
    return m


def echo(fp, args):
    return args.getlinstr('text', '')


def noquote(fp, args):
    return args.getlinstr('text', '')