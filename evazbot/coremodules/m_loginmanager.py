# -*- coding: utf-8 -*-
from base import *
import pickle
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


def getwlistlevel(nick):
    wlistlevelc = 0
    wlistlevelmc = 0
    for name in c_wlist.getw("whitelist"):
        for n in name[1]:
            if nick == n:
                wlistlevelc = name[0]
    try:
        wlistlevelmc = c_wlist.getcwlist()[nick]
    except KeyError:
        pass
    return max(wlistlevelc, wlistlevelmc)


def msg(mp):
    if mp.cmd("wlist"):
        try:
            level = int(mp.argstr("set"))
        except:
            main.sendcmsg("No argument!")
            return True
        if mp.argsdef() == mp.user():
            main.sendcmsg("You cannot set yourself.")
            return True
        if mp.iswlist(level + 1) and (getwlistlevel(mp.argsdef()) <
        getwlistlevel(mp.user())):
            c_wlist.getcwlist()[mp.argsdef()] = level
            main.sendcmsg(cmd.getname(mp.argsdef()) +
            " is now at level " + str(level))
        else:
            main.sendcmsg("You can only set: 0 to " +
            str(getwlistlevel(mp.user()) - 1))
            main.sendcmsg("The level of your target is: " +
            str(getwlistlevel(mp.argsdef())))
        save()
    if mp.cmd("login"):
        if mp.argbool("check"):
            nick = mp.argsdef().strip()
            if len(nick) == 0:
                nick = mp.user()
            wlistlevel = getwlistlevel(nick)
            main.sendcmsg(cmd.getname(nick) + ": Whitelist " + str(wlistlevel))
            adminlevel = 0
            try:
                for i in c_wlist.getw("adminlist"):
                    if main.ircprofiles[main.currentprofile][
                        "adminlist"][nick] == i[1]:
                            adminlevel = i[0]
            except KeyError:
                adminlevel = 0
            main.sendcmsg(cmd.getname(nick) + ": Admin " + str(adminlevel))

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
    main.sendcmsg(
        "-check [<nick>]: Check if you/<nick> are logged in as admin.")
    main.sendcmsg(".wlist -set=<level> nick:" +
    "Add a nick to the whitelist, -set defaults to 0.")