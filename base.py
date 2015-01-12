# -*- coding: utf-8 -*-
from imp import reload
import evazbot.main as main
import importlib
import os
import errno


def cload(module):
    m = importlib.import_module("evazbot.configs." + module)
    reload(m)
    return m


def mload(module):
    m = importlib.import_module("evazbot." + main.moduleset + "." + module)
    reload(m)
    return m


def mkpath(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

c_locs = c_redeclipse = cload("c_locs")
c_locs.lmoduleset = main.moduleset
cmd = cload("u_commands")
c_net = cload("c_net")
c_modules = cload("c_modules")
c_wlist = cload("c_wlist")
c_vars = cload("c_variables")