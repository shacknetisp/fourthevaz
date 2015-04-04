# -*- coding: utf-8 -*-
import configs.module


def init():
    m = configs.module.Module(__name__)
    m.set_help('View more messages.')
    m.add_command_hook('more',
        {
            'function': more,
            'help': 'Get next messages.',
            'args': [],
            })
    return m


def more(fp, args):
    if ('more.' + fp.outtarget()) in fp.server.state:
        try:
            return fp.server.state['more.' + fp.outtarget()].pop(0)
        except IndexError:
            pass
    return 'No more messages.'