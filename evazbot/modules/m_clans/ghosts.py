# -*- coding: utf-8 -*-
from base import *
import urllib
from urllib.request import urlopen

name = "Ghosts"
tag = "[" + name + "]"
leader = "Piggybear"
website = "http://ghostclanre.tk"
roster = website + "/roster"
rosterfile = roster + "/roster.txt"


def msg(mp):
    if mp.cmd("ghosts links"):
        main.sendcmsg("Website: " + website)
        main.sendcmsg("Roster: " + roster)
        return True
    elif mp.cmd("ghosts stats"):
        total_members = 0
        try:
            data = urlopen(rosterfile)
            for lineb in data:
                line = lineb.decode()
                if line.find("#") != 0 and line.find("|") != -1:
                    total_members += 1
            main.sendcmsg(name + " has " + str(total_members) + " members.")
        except urllib.error.URLError:
            main.sendcmsg("Cannot contact " + website)
        return True
    elif mp.cmd("ghosts"):
        main.sendcmsg(tag + " clan, lead by " + cmd.getname(leader) + ".")
        return True
    return False


def showhelp():
    main.sendcmsg(".ghosts: View information of the " + name + " clan.")
    main.sendcmsg(".ghosts links: View links to the " + name + " clan.")
    main.sendcmsg(".ghosts stats: View statistics of the " + name + " clan.")
