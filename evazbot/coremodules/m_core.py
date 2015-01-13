# -*- coding: utf-8 -*-
from base import *

modname = "Core"


def msg(mp, ct):
    if mp.acmd("mreload"):
        reload(c_modules)
        reload(c_wlist)
        import evazbot.irc as irc
        reload(irc)
        reload(cmd)
        c_modules.reloadall()
        return True

    if mp.acmd("remove", 99):
        args = mp.args()
        splitargs = args.split()
        if len(splitargs) == 1:
            r = c_modules.remove(splitargs[0])
            if not r:
                main.sendcmsg('Error while removing ' + splitargs[0])
            else:
                main.sendcmsg('Successfully removed ' + splitargs[0])
        else:
            main.sendcmsg("Invalid Arguments!")
        return True
    if mp.acmd("add"):
        args = mp.args()
        splitargs = args.split()
        if len(splitargs) == 1:
            if c_modules.astart(splitargs[0]):
                main.sendcmsg('Successfully added ' + splitargs[0])
            else:
                main.sendcmsg('Error while adding ' + splitargs[0])
        else:
            main.sendcmsg("Invalid Arguments!")
        return True
    if mp.acmd("dadd", 99):
        module = ct.args.getdef()
        if c_modules.astart(module):
            print((module + " is now active."))
        dmodules = []
        with open(c_modules.dbfile, 'r') as f:
            for line in f.readlines():
                if len(line.strip()) > 0:
                    dmodules.append(line.strip())
        if module not in dmodules:
            dmodules.append(module)
        dmodules2 = []
        for i in dmodules:
            dmodules2.append(i + '\n')
        with open(c_modules.dbfile, 'w') as f:
            f.writelines(dmodules2)
        print(('Added ' + module + ' to default list.'))
    if mp.acmd("dremove", 99):
        module = ct.args.getdef()
        if c_modules.remove(module):
            print('Removed ' + module + ' from active.')
        dmodules = []
        with open(c_modules.dbfile, 'r') as f:
            for line in f.readlines():
                if len(line.strip()) > 0:
                    dmodules.append(line.strip())
        dmodules = list(filter((module).__ne__, dmodules))
        dmodules2 = []
        for i in dmodules:
            dmodules2.append(i + '\n')
        with open(c_modules.dbfile, 'w') as f:
            f.writelines(dmodules2)
        print(('Removed ' + module + ' to default list.'))
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
