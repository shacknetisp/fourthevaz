# -*- coding: utf-8 -*-
from base import *

def msg(mp):
    if(mp.isserver()):
      return
    if mp.isjp("JOIN"):
        main.adminlist[mp.ircuser()]=""
        main.whois(mp.ircuser())
        main.sendamsg(cmd.getname(mp.ircuser()) + " is now in " + main.getchannel() + ".")
    elif mp.isjp("PART"):
        main.adminlist[mp.ircuser()]=""
        main.sendamsg(cmd.getname(mp.ircuser()) + " has departed " + main.getchannel() + ".")
    elif mp.isquit():
        main.adminlist[mp.ircuser()]=""
        main.sendamsg(cmd.getname(mp.ircuser()) + " has left IRC.")