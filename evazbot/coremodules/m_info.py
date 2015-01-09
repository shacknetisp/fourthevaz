# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from base import *

modname = "Info"
modcommand = "4e"


def msg(mp):
    modmessage = main.botname() + " is running. Use ." +\
    c_net.helpcommand + " for help."
    if mp.cmd(modcommand) or mp.cmd("info"):
        main.sendcmsg(modmessage)
        return True
    return False


def showhelp():
    main.sendcmsg(".4e OR .info: Confirm operation of " + c_net.name + ".")