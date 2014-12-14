import os
from os.path import expanduser
home = expanduser("~")

if os.name=="posix":
  rehome = home + "/.redeclipse"
  dbhome = home + "/.fourthevaz"
elif os.name=="nt":
  rehome = None
  dbhome = home + "/fourthevaz"
cmpath = "evazbot/modules/custom"