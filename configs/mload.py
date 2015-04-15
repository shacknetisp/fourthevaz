# -*- coding: utf-8 -*-
import importlib
import os
import sys
import imp
import configs.locs as locs
if locs.userdata not in sys.path:
    sys.path.append(locs.userdata)
import fnmatch


def find_module(name, path=None):
    for x in name.split('.'):
        if path is not None:
            path = [path]
        file, path, descr = imp.find_module(x, path)
    return path


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
    def skipname(n, folder):
        return n[0] == '_' or n in [
            'share',
            'sets',
        ] or fnmatch.fnmatch(n, '*.ext')
    server.modules = []
    paths = server.modulepaths()
    for path in paths:
        for f in os.listdir(path):
            if not skipname(f, path):
                server.add_module(os.path.splitext(f)[0])


def import_module_py(name, modulesets=[], doreload=True):
    possible = ['mlocal.']
    for mset in modulesets:
        possible.append('mlocal.sets.%s.' % mset)
        possible.append('modules.%s.' % mset)
    possible.append('modules.core.')
    m = None
    err = None
    for i in possible:
        try:
            if not find_module(i + name):
                continue
        except ImportError as e:
            err = e
            continue
        try:
            m = importlib.import_module(i + name)
        except ImportError as e:
            raise DepException(e)
        if not hasattr(m, 'init'):
            continue
        break
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
