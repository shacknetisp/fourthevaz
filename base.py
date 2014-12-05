# -*- coding: utf-8 -*-
import sys
import time
from imp import reload
import evazbot.main as main
import importlib


def cload(module):
    m = importlib.import_module("evazbot.configs." + module)
    reload(m)
    return m


def mload(module):
    m = importlib.import_module("evazbot.modules." + module)
    reload(m)
    return m


cmd = cload("u_commands")
c_net = cload("c_net")
c_modules = cload("c_modules")
c_locs = c_redeclipse = cload("c_locs")
c_wlist = cload("c_wlist")