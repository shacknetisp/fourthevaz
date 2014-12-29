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


def msg(mp):
    if mp.acmd("ircregister"):
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
        return True
    elif mp.acmd("ircverify"):
        main.sendmsg("nickserv", "VERIFY REGISTER " + main.ircprofiles[
        main.currentprofile]["nick"] + " " + mp.argsdef())
        return False
    elif mp.acmd("ircauth"):
        identify()
    return False


def showhelp():
    main.sendcmsg("You must define a password in profiles.py.")
    main.sendcmsg(
        ".ircregister <email>: Register this bot's current nick to <email>")
    main.sendcmsg(".ircverify <verify code>: Verify registration.")
    main.sendcmsg(".ircauth: Authenticate to Nickserv.")