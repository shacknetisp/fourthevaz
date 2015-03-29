# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module(__name__)
    m.set_help('Run tests.')
    m.add_command_hook('test',
        {
            'function': test,
            'help': 'Test stuff.',
            'args': [],
            })
    return m


def test(fp, args):
    fp.reply('\2this may be bold\2', 'NOTICE')