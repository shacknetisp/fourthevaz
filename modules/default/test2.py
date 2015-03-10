# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('test2')
    m.set_help('Run more tests.')
    m.add_command_hook('test',
        {
            'function': test,
            'help': 'Say "???", echo <echo> if specfied.',
            'args': {
                'echo': {
                    'optional': True,
                    'help': 'Echo this.',
                    }
                },
            })
    return m


def test(sp, args):
    print('???')
