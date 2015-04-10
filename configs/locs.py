# -*- coding: utf-8 -*-
import os
import sys
overridehome = ""
if len(sys.argv) > 1:
    overridehome = sys.argv[1]
from os.path import expanduser
home = expanduser("~")
if os.name == "posix":
    userdata = home + "/.fourthevaz"
elif os.name == "nt":
    userdata = home + "/fourthevaz"
elif not overridehome:
    raise ValueError('OS not supported.')
if len(overridehome) > 0:
    userdata = overridehome
cmoddir = userdata + '/mlocal'
os.makedirs(userdata, exist_ok=True)
userdb = userdata + '/db'
os.makedirs(userdb, exist_ok=True)
os.makedirs(cmoddir, exist_ok=True)
open(cmoddir + '/__init__.py', 'w').write('\n')
