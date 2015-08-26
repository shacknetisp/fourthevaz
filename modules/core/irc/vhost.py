# -*- coding: utf-8 -*-
from configs.module import Module


def init(options):
    m = Module('vhost')
    m.add_base_hook('joined', joined)
    return m


def joined(server):
    if server.auth[0] == 'vhost':
        if server.auth[1]:
            server.write_cmd(
                'VHOST', '%s %s' % (server.auth[1],
                    server.auth[2]))
        server.flush()
        server.setuser()
        server.join_channels()

