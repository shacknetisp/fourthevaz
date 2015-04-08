# -*- coding: utf-8 -*-
from configs.module import Module
import irc.utils
import importlib
importlib.reload(irc.utils)
from irc.utils import formatcodes


def init():
    m = Module(__name__)
    m.set_help('Run tests.')
    m.add_short_command_hook(test, 'test::Test.',
        [])
    return m


def test(fp, args):
    return (formatcodes.italic +
    'This is a%s test.' % formatcodes.reset)