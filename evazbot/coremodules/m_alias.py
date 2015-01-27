# -*- coding: utf-8 -*-
from base import *


def start():
    return ["alias", "echo"]


def msg(mp):
    if mp.wcmd("alias"):
        try:
            if mp.argbool('set'):
                main.aliasdb.data_dict[mp.argstr('set')] = mp.argsdef()
                main.sendcmsg("${%s} = '%s'" % (mp.argstr('set'), mp.argsdef()))
                main.aliasdb.save()
            elif mp.argbool('remove'):
                del main.aliasdb.data_dict[mp.argstr('remove')]
                main.sendcmsg("${%s} has been deleted" % (mp.argstr('remove')))
                main.aliasdb.save()
            else:
                main.sendcmsg("${%s} = '%s'" % (
                    mp.argsdef(), main.aliasdb.data_dict[mp.argsdef()]))
        except KeyError as e:
            main.sendcmsg("Invalid alias: %s" % e)
        return True
    elif mp.cmd("echo"):
        main.sendcmsg(mp.args())
    return False


def showhelp(h):
    h("alias [-set=<alias> -remove=<alias>] " +
    "<text for -set, alias for getting>: " +
    "Operate on an alias, accessible with ${<alias name>}.")
    h("echo <text>")