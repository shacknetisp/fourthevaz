# -*- coding: utf-8 -*-
from base import *
dbfile = c_locs.dbhome + "/wlist.db.pkl"


def load():
    try:
        dict_file = open(dbfile, 'rb')
        main.cwlist = pickle.load(dict_file)
        dict_file.close()
    except:
        pass


def save():
    output = open(dbfile, 'wb')
    pickle.dump(main.cwlist, output)
    output.close()

load()


def msg(mp):
    if mp.cmd("wlist"):
        try:
            level = int(mp.argstr("set"))
        except:
            level = 0
        main.cwlist[mp.argsdef()] = level
        main.sendcmsg(mp.argsdef() + " is now at level " + str(level))
        save()
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
            main.ircprofiles[main.currentprofile]["adminlist"][nick] = auth
            print(("Adding " + nick + " as " + auth))
    if mp.text().find("307") != -1\
        and (mp.text().find(":is identified for this nick") != -1 or
            mp.text().find(":is a registered nick") != -1 or
            mp.text().find(":has identified for this nick") != -1 or
            mp.text().find(":has identified for t\nhis nick") != -1):
            nick = mp.text().split()[3]
            auth = nick
            main.ircprofiles[main.currentprofile]["adminlist"][nick] = auth
            print(("Adding " + nick + " as " + auth))
    if mp.text().find("353 " + main.ircprofiles[
        main.currentprofile]["nick"]) != -1:
        for i in mp.text()[mp.text().index(":" + main.ircprofiles[
        main.currentprofile]["nick"]):].split():
            main.whois(i.strip("@"))


def showhelp():
    main.sendcmsg(".login [-check]: Login to this bot as admin.")
    main.sendcmsg("-check: Check if you are logged in as admin.")
    main.sendcmsg(".wlist -set=<level> nick:" +
    "Add a nick to the whitelist, -set defaults to 0.")