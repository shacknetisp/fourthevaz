# -*- coding: utf-8 -*-
from base import *
import subprocess
reload(subprocess)


def msg(mp):
    if mp.cmd("calc"):
        arg = mp.argsdef()
        if arg.find("read") == -1 or arg.find("help") == -1:
            p = subprocess.Popen("calc -- '" + arg + "'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            main.sendcmsg(out.decode().strip())
            main.sendcmsg(err.decode().strip())
        else:
            main.sendcmsg("Detected potentially harmful argument. Use math expressions only!")
        return True;
    return False

def showhelp():
    main.sendcmsg(".calc <mathematical expression>: Calculate a math expression.")