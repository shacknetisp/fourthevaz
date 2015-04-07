# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module(__name__)
    m.set_help('Run tests.')
    m.add_short_command_hook(test, 'test::Echo text.',
        ["[-before=string]::Echo this before <text>.",
        "text...::Echo this."])
    return m


def test(fp, args):
    return args.getlinstr('before', '') + ':' + args.getlinstr('text')