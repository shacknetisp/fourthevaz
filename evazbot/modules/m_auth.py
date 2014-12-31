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

lastauthuser = ""


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
        lastauthuser = mp.ircuser()
    if len(lastauthuser) > 0 and mp.ircuser().lower() == "nickserv":
        main.sendmsg(lastauthuser, mp.text().strip())
    return False


def showhelp():
    main.sendcmsg("You must define a password in profiles.py.")
    main.sendcmsg(
        ".ircregister <email>: Register this bot's current nick to <email>")
    main.sendcmsg(".ircverify <verify code>: Verify registration.")
    main.sendcmsg(".ircauth: Authenticate to Nickserv.")