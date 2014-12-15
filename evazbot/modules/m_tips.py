# -*- coding: utf-8 -*-
from base import *
import sys
import random

dbfile = c_redeclipse.dbhome + "/tips.db.txt"


def msg(mp):
    if mp.wcmd("addtip"):
        args = mp.args("addtip")
        with open(dbfile, "a") as myfile:
            myfile.write(args + "\n")
            main.sendcmsg("Tip added: " + args)
        return True
    if mp.cmd("tip"):
        args = mp.args("tip")
        lines = []
        for line in open(dbfile, 'r'):
            lines.append(line.strip())
        out = random.choice(lines)
        outfull = str.format('Tip: "{0}"', out)
        main.sendcmsg(outfull)
        return True
    if mp.wcmd("sorttips"):
        lines = []
        for line in open(dbfile, 'r'):
            lines.append(line)
        lines.sort()
        with open(dbfile, 'w') as f:
            f.writelines(lines)
        main.sendcmsg("The tips have been sorted.")
        return True
    return False


def showhelp():
    main.sendcmsg(
        ".tip: Recall random tip..")
    main.sendcmsg(".addtip <the tip>: Add <the tip>.")
    main.sendcmsg(".sorttips: Clean the tip DB.")
