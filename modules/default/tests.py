# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('tests')
    m.set_help('Run tests.')
    m.add_command_hook('test',
        {
            'function': test,
            'help': 'Say "!!!", echo if specfied.',
            'args': [
                {
                    'name': 'echo',
                    'optional': True,
                    'help': 'Echo this.',
                    }
                ],
            })
    return m


def test(fp, args):
    print('!!')
