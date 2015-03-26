# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('tests')
    m.set_help('Run tests.')
    m.add_command_hook('test',
        {
            'function': test,
            'help': 'Test stuff.',
            'args': [
                {
                    'name': 'target',
                    'optional': False,
                    'help': 'target',
                    },
                {
                    'name': 'echo',
                    'optional': False,
                    'help': 'text to echo',
                    'end': True,
                    }
                ],
            })
    return m

def test(fp, args):
    return args.getlinstr('target') + ": " + args.getlinstr('echo')