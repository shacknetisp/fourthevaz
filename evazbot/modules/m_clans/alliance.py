# -*- coding: utf-8 -*-
from base import *
import urllib
from urllib.request import urlopen

name = "Alliance"
tag = name + " |"
leader = "Sharidan2214"
website = "http://allianceclan.iclanwebsites.com"


def msg(mp):
    if mp.cmd("alliance links"):
        main.sendcmsg("Website: " + website)
        return True
    elif mp.cmd("alliance"):
        main.sendcmsg(tag + " clan, lead by " + cmd.getname(leader) + ".")
        return True
    return False


def showhelp():
    main.sendcmsg(".alliance: View information of the " + name + " clan.")
    main.sendcmsg(".alliance links: View links to the " + name + " clan.")
