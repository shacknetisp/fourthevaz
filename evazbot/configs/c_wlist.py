# -*- coding: utf-8 -*-
from base import *
exec(open(c_locs.dbhome + "/wlist.py").read())


def getw(l):
    return profiles[main.ircprofiles[main.currentprofile]['whitelist']][l]


def getcwlist():
    w = main.ircprofiles[main.currentprofile]['whitelist']
    if w not in main.cwlist:
        main.cwlist[w] = {}
    return main.cwlist[w]


