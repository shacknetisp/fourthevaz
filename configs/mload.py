# -*- coding: utf-8 -*-
import importlib
import os
import moduleregistry
globalmodules = []


def serverinit(server):
    server.modules += globalmodules
    for f in os.listdir('modules/%s/' % server.entry['moduleset']):
        if f[0] != '_':
            m = import_module(
                os.path.splitext(f)[0], server.entry['moduleset'])
            server.modules.append(m)


def import_module(name, moduleset=""):
    m = importlib.import_module(
        'modules.%s.' % moduleset + name)
    moduleregistry.delete_module(m)
    moduleregistry.add_module(m)
    m = m.init()
    print(('Loaded: %s, Hooks: %s%s' % (
        name,
        str(list(m.base_hooks.keys())),
        str(list(m.command_hooks.keys())),
        )))
    return m


def loadcore():
    for f in os.listdir('modules/core/'):
        if f[0] != '_':
            m = import_module(os.path.splitext(f)[0], "core")
            globalmodules.append(m)