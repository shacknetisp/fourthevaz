# -*- coding: utf-8 -*-
from base import *

modname = "Core"


def start():
    return [
        "mreload",
        "module",
        "join",
        "part",
        ]


def msg(mp, ct):
    if mp.acmd("mreload"):
        reload(c_modules)
        reload(c_wlist)
        import evazbot.irc as irc
        reload(irc)
        reload(cmd)
        c_modules.reloadall()
        return True

    if ct.cmd('m', 0, 99):
        if ct.args.getbool('add'):
            module = ct.args.getdef()
            if c_modules.astart(module):
                print((module + " is now active."))
            ct.msg('Added %s' % module)
        elif ct.args.getbool('remove'):
            module = ct.args.getdef()
            if c_modules.remove(module):
                print(("Removed " + module + " from active."))
            ct.msg('Removed %s' % module)
        elif ct.args.getbool('dadd'):
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
            ct.msg(('Added ' + module + ' to default list.'))
        elif ct.args.getbool('dremove'):
            module = ct.args.getdef()
            if c_modules.remove(module):
                print(("Removed " + module + " from active."))
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
            ct.msg(('Removed ' + module + ' from default list.'))
        else:
            ct.msg('Invalid arguments')
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


def showhelp(h):
    h("mreload: Stop modules & reload default modules.")
    h("m [-add -remove -dadd -dremove] <m>: Operate on module <m>")
    h("join #channel")
    h("part #channel")

whitelistreload = 0


def tick():
    global whitelistreload
    whitelistreload += 1
    if whitelistreload >= 5:
        reload(c_wlist)
        whitelistreload = 0
