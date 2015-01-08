import os
import sys
overridehome = ""
if len(sys.argv) > 1:
    overridehome = sys.argv[1]
from os.path import expanduser
home = expanduser("~")

if os.name == "posix":
    rehome = home + "/.redeclipse"
    dbhome = home + "/.fourthevaz"
elif os.name == "nt":
    rehome = home + "/Documents/My Games/Red Eclipse/"
    dbhome = home + "/fourthevaz"
if len(overridehome) > 0:
    dbhome = overridehome
cmpath = "evazbot/modules/custom"
mconfigpath = dbhome + "/mconfig"


def mconfig(m):
    try:
        return open(mconfigpath + "/" + m + ".py").read()
    except:
        return ""