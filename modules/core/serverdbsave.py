# -*- coding: utf-8 -*-
from configs.module import Module
import running


def init(options):
    m = Module('serverdbsave')
    m.set_help('Save the server databases.')
    m.add_timer_hook(10 * 1000, timer)
    return m


def timer():
    running.serverdb.save()
    for e in running.accesslist.db():
        d = running.accesslist.db()[e]
        tod = []
        for name in d:
            if not d[name]:
                tod.append(name)
        for todi in tod:
            del d[todi]
    running.accesslist.save()

