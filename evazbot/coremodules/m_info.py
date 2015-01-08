# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from base import *

modname = "Info"
modcommand = "4e"
modmessage = c_net.name + " is running. Use ." +\
    c_net.helpcommand + " for help."


def msg(mp):
    if mp.cmd(modcommand) or mp.cmd("info"):
        main.sendcmsg(modmessage)
        return True
    elif mp.text().find("\x01VERSION\x01") != -1:
        main.sendcmsg("\x01" +
        "VERSION " +
        "Fourth Evaz IRC Bot.",
        "NOTICE")
        return True
    return False


def showhelp():
    main.sendcmsg(".4e OR .info: Confirm operation of " + c_net.name + ".")