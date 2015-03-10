# -*- coding: utf-8 -*-
import importlib
import os
import moduleregistry
globalmodules = []


def serverinit(server):
    server.modules += globalmodules
    for f in os.listdir('modules/%s/' % server.moduleset):
        if f[0] != '_':
            m = import_module(f.strip('.py'), server.moduleset)
            server.modules.append(m)


def import_module(name, moduleset=""):
    if moduleset:
        m = importlib.import_module('modules.core.' + name)
    else:
        m = importlib.import_module(
            'modules.%s.' % moduleset + name)
    moduleregistry.delete_module(m)
    moduleregistry.add_module(m)
    print(('Loaded: %s' % name))
    return m.init()


def loadcore():
    for f in os.listdir('modules/core/'):
        if f[0] != '_':
            m = import_module(f.strip('.py'), "core")
            globalmodules.append(m)