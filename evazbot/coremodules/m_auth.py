# -*- coding: utf-8 -*-
from base import *


def identify(i=False):
    try:
        main.sendmsg("nickserv", "IDENTIFY " + main.password)
    except:
        if i:
            print("Unable to identify, no password set.")
        else:
            main.sendcmsg("Unable to identify, no password set.")


def joined():
    identify(True)
    return False

lastauthuser = {}


def start():
    return [
        "ircregister",
        "ircverify",
        "ircauth"
        ]


def get(ct):
    global lastauthuser
    usedcmd = False
    if ct.cmd("ircregister", 1, 1):
        usedcmd = True
        try:
            password = main.password
            if len(ct.args.getdef()) == 0:
                ct.msg("No e-mail address specified.")
            else:
                ct.msg("REGISTER " +
                password + " " + ct.args.getdef(), "nickserv")
        except:
            main.sendcmsg("Unable to register, no password set.")
    elif ct.cmd("ircverify", 1, 1):
        usedcmd = True
        ct.msg("VERIFY REGISTER " + ct.botnick() + " " + ct.args.getdef(),
        "NickServ")
    elif ct.cmd("ircauth", 1, 1):
        usedcmd = True
        identify()
    if usedcmd:
        lastauthuser[main.currentprofile] = ct.ircuser()
    try:
        if (len(lastauthuser[main.currentprofile]) > 0 and
        ct.ircuser() == "NickServ"):
            ct.msg(ct.text(), lastauthuser[main.currentprofile])
    except KeyError:
        pass
    return False


def showhelp(h):
    main.sendcmsg("You must define a password in profiles.py.")
    h("ircregister <email>: Register this bot's current nick to <email>")
    h("ircverify <verify code>: Verify registration.")
    h("ircauth: Authenticate to Nickserv.")