# -*- coding: utf-8 -*-
from configs.module import Module
import shlex


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
    m.add_command_hook('bold',
        {
            'function': bold,
            'help': 'Echo bold text.',
            'args': [
                {
                    'name': 'text',
                    'optional': False,
                    'help': 'Text to echo bolded.',
                    'end': True,
                    },
                ],
            })
    m.add_command_hook('noquote',
        {
            'function': noquote,
            'noshlex': True,
            'help': 'Quote text for shlex.',
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


def bold(fp, args):
    return "\2%s\2" % args.getlinstr('text', '')


def noquote(fp, args):
    return shlex.quote(args.getlinstr('text', ''))