# -*- coding: utf-8 -*-
from configs.module import Module
import running
import time


def init(options):
    options['server'].state['lastpong'] = time.time()
    m = Module('ping')
    m.set_help('Reply to PING messages from the IRC server.')
    m.add_base_hook('recv', recv)
    m.add_timer_hook(10 * 1000, timer)
    return m


def recv(fp):
    try:
        if fp.sp.splitmessage[0].upper() == 'PING':
            fp.server.write_cmd('PONG', fp.sp.splitmessage[1])
        elif fp.sp.splitmessage[1].upper() == 'PONG':
            fp.server.state['lastpong'] = time.time()
    except IndexError:
        pass


def timer():
    for server in running.working_servers:
        if time.time() - server.state['lastpong'] > 15:
            server.write_cmd('PING', server.nick)
        if time.time() - server.state['lastpong'] > 30:
            server.socket.close()

