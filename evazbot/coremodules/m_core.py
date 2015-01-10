# -*- coding: utf-8 -*-
from base import *

modname = "Core"


def start():
    c_wlist.load()


def msg(mp):
    if mp.acmd("mreload"):
        reload(c_modules)
        reload(c_wlist)
        c_modules.reloadall()
        return True

    if mp.acmd("remove", 99):
        args = mp.args()
        splitargs = args.split()
        if len(splitargs) == 1:
            r = c_modules.remove(splitargs[0])
            if not r:
                main.sendcmsg("Couldn't remove module!")
        else:
            main.sendcmsg("Invalid Arguments!")
        return True
    if mp.acmd("add"):
        args = mp.args()
        splitargs = args.split()
        if len(splitargs) == 1:
            c_modules.astart(splitargs[0])
        else:
            main.sendcmsg("Invalid Arguments!")
        return True
    if mp.acmd("dadd", 99):
        args = mp.args()
        splitargs = args.split()
        if len(splitargs) == 1:
            lines = []
            for line in open(c_modules.dbfile, "r"):
                if line.split() != splitargs[0].split():
                    lines.append(line)
            lines.append(splitargs[0])
            lines.append("\n")
            with open(c_modules.dbfile, "w") as f:
                f.writelines(lines)
            c_modules.astart(splitargs[0])
            c_modules.reloadall()
        return True
    if mp.acmd("dremove", 99):
        args = mp.args()
        splitargs = args.split()
        if len(splitargs) == 1:
            lines = []
            try:
                for line in open(c_modules.dbfile, "r"):
                    if line.split() != splitargs[0].split():
                        lines.append(line)
            except FileNotFoundError:
                main.sendcmsg("Module does not exist!")
                return True
            r = c_modules.remove(splitargs[0])
            if not r:
                main.sendcmsg("Module does not exist!")
            else:
                c_modules.reloadall()
        else:
            main.sendcmsg("Invalid Arguments!")
        return True

    if mp.acmd("join", 99):
        channel = mp.argsdef()
        main.ircprofiles[main.currentprofile]['channels'].append(channel)
        main.joinchan(channel)
        main.sendcmsg('Attempted to join channel ' + channel)
        return True

    if mp.acmd("part", 99):
        channel = mp.argsdef()
        main.ircwrite('PART ' + channel)
        main.sendcmsg('Attempted to part channel ' + channel)
        return True
    return False


def showhelp():
    main.sendcmsg(cmd.cprefix() +
    "mreload: Stop modules & reload default modules.")
    main.sendcmsg(
        cmd.cprefix() +
        "add <m>: Load & start module <m>. If <m> is running, stop it.")
    main.sendcmsg(cmd.cprefix() + "remove <m>: Unload module <m>.")
    main.sendcmsg(cmd.cprefix() + "dadd <m>: Add module to the defaults list.")
    main.sendcmsg(cmd.cprefix() +
    "dremove <m>: Remove module from the defaults list.")
    main.sendcmsg(cmd.cprefix() + "join #channel")
    main.sendcmsg(cmd.cprefix() + "part #channel")

whitelistreload = 0


def tick():
    global whitelistreload
    whitelistreload += 1
    if whitelistreload >= 5:
        reload(c_wlist)
        whitelistreload = 0
