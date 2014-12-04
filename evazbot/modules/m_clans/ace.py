# -*- coding: utf-8 -*-
from base import *
import urllib
from urllib.request import urlopen

name = "ACE"
tag = "*" + name + "*"
leader = "Duck"
website = "http://reaceclan.tk/"


def msg(mp):
    if mp.cmd("ace links"):
        main.sendcmsg("Website: " + website)
        return True
    elif mp.cmd("ace"):
        main.sendcmsg(tag + " clan, lead by " + cmd.getname(leader) + ".")
        return True
    return False


def showhelp():
    main.sendcmsg(".ace: View information of the " + name + " clan.")
    main.sendcmsg(".ace links: View links to the " + name + " clan.")
