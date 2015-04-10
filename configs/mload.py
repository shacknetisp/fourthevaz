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


class DepException(Exception):

    def __init__(self, e):
        self.e = e

    def __str__(self):
        return str(self.e)


def serverinit(server):
    def skipname(n):
        return n[0] == '_' or n == 'share'
    server.modules = []
    for f in os.listdir(locs.cmoddir):
        if not skipname(f):
            server.add_module(os.path.splitext(f)[0])
    for mset in server.entry['modulesets']:
        try:
            for f in os.listdir(locs.cmoddir + '/%s' % mset):
                if not skipname(f):
                    server.add_module(os.path.splitext(f)[0])
        except FileNotFoundError:
            continue
    for f in os.listdir('modules/%s/' % "core"):
        if not skipname(f):
            server.add_module(os.path.splitext(f)[0])
    for mset in server.entry['modulesets']:
        try:
            for f in os.listdir('modules/%s/' % mset):
                if not skipname(f):
                    server.add_module(os.path.splitext(f)[0])
        except FileNotFoundError:
            continue


def import_module_py(name, modulesets=[], doreload=True):
    possible = ['mlocal.']
    for mset in modulesets:
        possible.append('mlocal.%s.' % mset)
        possible.append('modules.%s.' % mset)
    possible.append('modules.core.')
    m = None
    err = None
    for i in possible:
        try:
            m = importlib.import_module(i + name)
            if not hasattr(m, 'init'):
                continue
            break
        except ImportError as e:
            err = e
            if e.name.split('.')[0] not in ['mlocal', 'modules']:
                raise DepException(e)
    if not m:
        raise err
    if not os.path.exists(m.__file__):
        raise DDRException(name)
    if doreload:
        importlib.reload(m)
    return m


def import_module(name, modulesets=[], doreload=True, options={}):
    m = import_module_py(name, modulesets, doreload)
    if m.init.__code__.co_argcount == 1:
        mr = m.init(options)
    else:
        mr = m.init()

    mr.module = m
    print(('Loaded: %s: %s, Hooks: %s%s' % (
        name,
        str(m),
        str(list(mr.base_hooks.keys())),
        str(list(mr.command_hooks.keys())),
        )))
    return mr
