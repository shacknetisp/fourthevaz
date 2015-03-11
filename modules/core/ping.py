# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('ping')
    m.set_help('Reply to PING messages from the IRC server.')
    m.add_base_hook('recv', recv)
    return m


def recv(fp):
    if fp.sp.splitmessage[0].upper() == 'PING':
        fp.server.write_cmd('PONG', fp.sp.splitmessage[1])

