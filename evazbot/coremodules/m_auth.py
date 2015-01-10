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


def msg(mp):
    global lastauthuser
    usedcmd = False
    if mp.acmd("ircregister"):
        usedcmd = True
        try:
            password = main.password
            print(("Registering for password: " + password))
            if len(mp.argsdef()) == 0:
                main.sendcmsg("No e-mail address specified.")
            else:
                main.sendmsg("nickserv", "REGISTER " +
                password + " " + mp.argsdef())
        except:
            main.sendcmsg("Unable to register, no password set.")
    elif mp.acmd("ircverify"):
        usedcmd = True
        main.sendmsg("nickserv", "VERIFY REGISTER " + main.ircprofiles[
        main.currentprofile]["nick"] + " " + mp.argsdef())
    elif mp.acmd("ircauth"):
        usedcmd = True
        identify()
    if usedcmd:
        lastauthuser[main.currentprofile] = mp.ircuser()
    try:
        if (len(lastauthuser[main.currentprofile]) > 0 and
        mp.ircuser().lower() == "nickserv"):
            main.sendmsg(lastauthuser[main.currentprofile], mp.text().strip())
    except KeyError:
        pass
    return False


def showhelp():
    main.sendcmsg("You must define a password in profiles.py.")
    main.sendcmsg(
        cmd.cprefix +
        "ircregister <email>: Register this bot's current nick to <email>")
    main.sendcmsg(cmd.cprefix +
    "ircverify <verify code>: Verify registration.")
    main.sendcmsg(cmd.cprefix + "ircauth: Authenticate to Nickserv.")