# -*- coding: utf-8 -*-
from base import *


def msg(mp):
    if mp.cmd("login"):
        if mp.argbool("check"):
            if mp.isadmin() and mp.iswlist():
                main.sendcmsg("You are an admin.")
            elif mp.iswlist():
                main.sendcmsg("You are whitelisted.")
            else:
                main.sendcmsg("You have no authentication.")
        else:
            main.whois(mp.ircuser())
            main.sendcmsg("Login attempt processed.")
    if mp.text().find("330") != -1\
        and mp.text().find(":is logged in as") != -1:
            nick = cmd.find_between(
                mp.text(), " ", ":is logged in as").split()[2]
            auth = cmd.find_between(
                mp.text(), " ", ":is logged in as").split()[3]
            main.adminlist[nick] = auth
            print(("Adding " + nick + " as " + auth))
    if mp.text().find("353 " + main.ircprofiles[
        main.currentprofile]["nick"]) != -1:
        for i in mp.text().split():
            main.whois(i.strip("@"))


def showhelp():
    main.sendcmsg(".login [-check]: Login to this bot as admin.")
    main.sendcmsg("-check: Check if you are logged in as admin.")