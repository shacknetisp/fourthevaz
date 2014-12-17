# -*- coding: utf-8 -*-
#This will import all essential Fourth Evaz components
from base import *


def msg(mp):
    if mp.cmd("example"):
        main.sendcmsg("Example's Arguments: " + mp.args())


def showhelp():
    main.sendcmsg(".example <arguments>: Return the arguments.")