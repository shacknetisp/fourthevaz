# -*- coding: utf-8 -*-
from base import *
import subprocess
reload(subprocess)


def msg(mp):
    if mp.cmd("fortune"):
        p = subprocess.Popen("fortune -n 40", shell=True,
          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        main.sendcmsg(out.decode().strip().replace("\n", " "))
    return False


def showhelp():
    main.sendcmsg(".fortune: Get a random fortune.")