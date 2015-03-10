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
else:
    raise ValueError('OS not supported.')
if len(overridehome) > 0:
    userdata = overridehome
