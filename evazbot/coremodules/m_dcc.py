# -*- coding: utf-8 -*-
from base import *
welcome = "Hello {user}, you are accessing DCC with a level of {wlist}. " + \
"No commands are supported yet."

##mconfig/ctcp.py
##lines of the following:
#welcome = "Hello {user}, you are accessing DCC with a level of {wlist}."
exec(c_locs.mconfig("dcc"))


def dccconnect(dcc):
    dcc.send(welcome.format(**{
        'user': dcc.nick,
        'wlist': str(dcc.wlistlevel),
        }))


def dccget(dcc, text):
    return

