# -*- coding: utf-8 -*-
import sys
import os
overridehome = ""
if len(sys.argv) > 1:
    overridehome = sys.argv[1]
userdata = './userdata'
"""User data folder."""
if len(overridehome) > 0:
    userdata = overridehome
cmoddir = userdata + '/mlocal'
os.makedirs(userdata, exist_ok=True)
userdb = userdata + '/db'
"""User DB folder, store module data here or in Server.db."""
os.makedirs(userdb, exist_ok=True)
os.makedirs(cmoddir, exist_ok=True)
open(cmoddir + '/__init__.py', 'w').write('\n')
