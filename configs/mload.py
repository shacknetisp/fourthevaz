# -*- coding: utf-8 -*-
import importlib
import os
import sys
import configs.locs as locs
if locs.userdata not in sys.path:
    sys.path.append(locs.userdata)


class DDRException(Exception):

    def __init__(self, m):
        self.m = m

    def __str__(self):
        return "Module %s was deleted while running." % self.m


def serverinit(server):
    server.modules = []
    for f in os.listdir(locs.cmoddir):
        if f[0] != '_':
            server.add_module(os.path.splitext(f)[0])
    for f in os.listdir('modules/%s/' % "core"):
        if f[0] != '_':
            server.add_module(os.path.splitext(f)[0])
    for f in os.listdir('modules/%s/' % server.entry['moduleset']):
        if f[0] != '_':
            server.add_module(os.path.splitext(f)[0])


def import_module_py(name, moduleset="", doreload=True):
    possible = ['mlocal.', 'modules.core.', 'modules.%s.' % moduleset]
    m = None
    err = None
    for i in possible:
        try:
            m = importlib.import_module(i + name)
            break
        except ImportError as e:
            err = e
    if not m:
        raise err
    if not os.path.exists(m.__file__):
        raise DDRException(name)
    if doreload:
        importlib.reload(m)
    return m


def import_module(name, moduleset="", doreload=True):
    m = import_module_py(name, moduleset, doreload)
    mr = m.init()

    mr.module = m
    print(('Loaded: %s: %s, Hooks: %s%s' % (
        name,
        str(m),
        str(list(mr.base_hooks.keys())),
        str(list(mr.command_hooks.keys())),
        )))
    return mr
