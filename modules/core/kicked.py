# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module()
    m.add_base_hook('recv', recv)
    return m


def recv(fp):
    if fp.sp.iscode('kick') and fp.sp.object == fp.server.nick:
        fp.server.join_channel(fp.sp.target)
