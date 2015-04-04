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
    if ('more.' + fp.sp.sendernick) in fp.server.state:
        try:
            m = (fp.server.state['more.' + fp.sp.sendernick].pop(0))
            if fp.server.state['more.%s' % fp.sp.sendernick]:
                l = len(fp.server.state['more.%s' % fp.sp.sendernick])
                m += ' \2(%d more message%s)\2' % (l,
                    's' if l != 1 else '')
            return m
        except IndexError:
            pass
    return 'No more messages.'