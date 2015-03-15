# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('tests')
    m.set_help('Run tests.')
    m.add_command_hook('test',
        {
            'function': test,
            'help': 'Test stuff.',
            'args': [],
            })
    return m


def test(fp, args):
    fp.server.socket.close()