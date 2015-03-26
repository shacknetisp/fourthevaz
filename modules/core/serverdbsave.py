# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from configs.module import Module
import running


def init(options):
    m = Module('serverdbsave')
    m.set_help('Save the server databases.')
    m.add_timer_hook(10 * 1000, timer)
    return m


def timer():
    for server in running.working_servers:
        server.db.save()

