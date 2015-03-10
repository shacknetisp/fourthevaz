# -*- coding: utf-8 -*-
from importlib import reload
registry = []


def delete_module(m):
    global registry
    registry = list(filter((m).__ne__, registry))


def add_module(m):
    global registry
    if m in registry:
        return
    registry.append(m)
    reload(m)


def reload_all():
    global registry
    for m in registry:
        reload(m)