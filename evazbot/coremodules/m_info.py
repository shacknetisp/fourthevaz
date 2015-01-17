# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from base import *


def start():
    return [
        "4e",
        "info",
        ]


def msg(mp):
    modmessage = main.botname() + " is running. Use " +\
    cmd.cprefix() + "help for help."
    if mp.cmd("4e") or mp.cmd("info"):
        main.sendcmsg(modmessage)
        return True
    return False


def showhelp():
    main.sendcmsg(cmd.cprefix() + "4e OR " +
    cmd.cprefix() + "info: Confirm operation of " + c_net.name + ".")