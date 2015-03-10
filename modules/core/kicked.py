# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('kicked')
    m.set_help('Rejoin a channel when kicked.')
    m.add_base_hook('recv', recv)
    return m


def recv(fp):
    if fp.sp.iscode('kick') and fp.sp.object == fp.server.nick:
        fp.server.join_channel(fp.sp.target)
