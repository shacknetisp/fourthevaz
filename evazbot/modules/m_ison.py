# -*- coding: utf-8 -*-
from base import *

defaultsearch = "ghosts"


def msg(mp):
    if mp.cmd("ison"):
        args = mp.args("ison")
        splitargs = args.split()
        main.sendcmsg("ison:")
        search = defaultsearch
        if splitargs >= 1:
            search = args
        else:
            main.sendcmsg("Invalid Arguments!")
        return True
    return False


"""
def help():
  time.sleep(0.25)
  main.sendcmsg(".ison name of player: Search play.redeclipse.net for <name>.")
"""