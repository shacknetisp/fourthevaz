# -*- coding: utf-8 -*-
from base import *
import random
import time

dbfile = c_redeclipse.dbhome + "/hist.db.txt"


def msg(mp):
    now = time.strftime("%d/%m/%Y %H:%M:%S")
    if mp.wcmd("addhist"):
        args = mp.args("addhist")
        with open(dbfile, "a") as myfile:
            myfile.write(now + ": " + args + "\n")
            main.sendcmsg("History added: " + now + ": " + args)
        return True
    if mp.cmd("hist"):
        args = mp.args("hist")
        lines = []
        for line in open(dbfile, 'r'):
            lines.append(line.strip())
        out = random.choice(lines)
        outfull = str.format('{0}', out)
        main.sendcmsg(outfull)
        return True
    if mp.wcmd("sorthist"):
        lines = []
        for line in open(dbfile, 'r'):
            lines.append(line)
        lines.sort()
        with open(dbfile, 'w') as f:
            f.writelines(lines)
        main.sendcmsg("The history DB has been sorted.")
        return True
    return False


def showhelp():
    main.sendcmsg(
        cmd.cprefix + "hist: Recall random history bit.")
    main.sendcmsg(cmd.cprefix + "addhist <history>: Add <history> to the DB.")
    main.sendcmsg(cmd.cprefix + "sorthist: Clean the history DB.")
