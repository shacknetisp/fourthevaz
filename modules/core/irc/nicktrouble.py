# -*- coding: utf-8 -*-
from configs.module import Module
import random


def init():
    m = Module('nicktrouble')
    m.set_help('Handle when the nick is taken.')
    m.add_base_hook('recv', recv)
    m.add_base_hook('nicktrouble', nicktrouble)
    return m


def nicktrouble(server):
    if not server.auth:
        server.nick += str(random.randrange(0, 100))
        server.setuser()


def recv(fp):
    if fp.sp.iscode('433'):
        fp.server.do_base_hook('nicktrouble', fp.server)

