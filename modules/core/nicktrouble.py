# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('nicktrouble')
    m.set_help('Handle when the nick is taken.')
    m.add_base_hook('recv', recv)
    return m


def recv(fp):
    if fp.sp.iscode('433'):
        if fp.server.auth[0] == 'nickserv':
            wantnick = fp.server.entry['id']['nick']
            fp.server.nick = fp.server.nick + '_'
            fp.server.setuser()
            fp.server.write_cmd('PRIVMSG',
                    'nickserv :identify %s %s' % (
                    wantnick,
                    fp.server.auth[2]))
            fp.server.write_cmd('PRIVMSG',
                'nickserv :ghost %s %s' % (
                    wantnick,
                    fp.server.auth[2]))
            fp.server.nick = wantnick
            fp.server.setuser()
        else:
            fp.server.nick += '_'
        fp.server.setuser()
