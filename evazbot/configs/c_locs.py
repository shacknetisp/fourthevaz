import os
from os.path import expanduser
home = expanduser("~")

if os.name == "posix":
    rehome = home + "/.redeclipse"
    dbhome = home + "/.fourthevaz"
elif os.name == "nt":
    rehome = home + "/Documents/My Games/Red Eclipse/"
    dbhome = home + "/fourthevaz"
cmpath = "evazbot/modules/custom"