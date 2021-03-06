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
            'irc',
        ] or fnmatch.fnmatch(n, '*.ext')
    server.modules = []
    paths = server.modulepaths()
    for path in paths:
        for f in os.listdir(path):
            if not skipname(f, path):
                server.add_module(os.path.splitext(f)[0])


def import_module_py(name, modulesets=[],
    protocol='irc', doreload=True, ret={}):
    possible = [['mlocal.']]
    for mset in modulesets:
        possible.append(('mlocal.sets.%s.' % mset, mset))
        possible.append(('modules.%s.' % mset, mset))
    possible.append(['modules.core.', 'core'])
    p2 = []
    for p in possible:
        if len(p) == 2:
            p2.append((p[0] + '%s.' % protocol, p[1]))
        else:
            p2.append([p[0] + '%s.' % protocol])
    possible += p2
    m = None
    err = None
    usedset = ""
    for i in possible:
        try:
            if not find_module(i[0] + name):
                continue
        except ImportError as e:
            err = e
            continue
        try:
            m = importlib.import_module(i[0] + name)
            if len(i) == 2:
                usedset = i[1]
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
    ret['usedset'] = usedset
    return m


def import_module(name, modulesets=[], protocol='irc',
    doreload=True, options={}):
    e = {}
    m = import_module_py(name, modulesets, protocol, doreload, e)
    if m.init.__code__.co_argcount == 1:
        mr = m.init(options)
    else:
        mr = m.init()
    if not mr:
        return None
    mr.set = e['usedset']
    mr.module = m
    print(('Loaded: %s (%s): %s, Hooks: %s%s' % (
        name,
        mr.set,
        str(m),
        str(list(mr.base_hooks.keys())),
        str(list(mr.command_hooks.keys())),
        )))
    return mr
