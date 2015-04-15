# -*- coding: utf-8 -*-
import configs.module
import irc.utils


def init():
    m = configs.module.Module(__name__)
    m.set_help('View more messages.')
    m.add_command_hook('more',
        {
            'function': more,
            'help': 'Get next messages.',
            'args': [],
            })
    m.add_short_command_hook(clearmore,
        'clearmore::Clear next messages.', [])
    return m


def more(fp, args):
    if ('more.' + fp.user) in fp.server.state:
        try:
            m = (fp.server.state['more.' + fp.user].pop(0))
            if fp.server.state['more.%s' % fp.user]:
                l = len(fp.server.state['more.%s' % fp.user])
                m += (' ' + irc.utils.formatcodes.bold +
                '(%d more message%s)' % (l,
                's' if l != 1 else ''))
            fp.moreflag = True
            return m
        except IndexError:
            pass
    return 'No more messages.'


def clearmore(fp, args):
    if ('more.' + fp.user) in fp.server.state:
        l = len(fp.server.state['more.' + fp.user])
        del fp.server.state['more.' + fp.user]
        return 'Cleared %d message%s.' % (l, '' if l == 1 else 's')
    return 'No more messages.'