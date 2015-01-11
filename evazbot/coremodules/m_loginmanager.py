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


def msg(mp, ct):
    if ct.cmd("wlist"):
        try:
            level = int(ct.args.get("set"))
        except:
            main.sendcmsg("No argument!")
            return True
        if ct.args.getdef() == ct.user():
            ct.msg("You cannot set yourself.")
            return True
        if ct.islogin(level + 1) and (getwlistlevel(mp.argsdef()) <
        getwlistlevel(ct.user())):
            c_wlist.getcwlist()[mp.argsdef()] = level
            main.sendcmsg(cmd.getname(mp.argsdef()) +
            " is now at level " + str(level))
        else:
            main.sendcmsg("You can only set: 0 to " +
            str(getwlistlevel(mp.user()) - 1))
            main.sendcmsg("The level of your target is: " +
            str(getwlistlevel(mp.argsdef())))
        save()
    if ct.cmd("login"):
        if ct.args.getbool("check"):
            nick = ct.args.getdef().strip()
            if len(nick) == 0:
                nick = ct.user()
            wlistlevel = getwlistlevel(nick)
            ct.msg(cmd.getname(nick) + ": Whitelist " + str(wlistlevel))
            adminlevel = 0
            try:
                for i in c_wlist.getw("adminlist"):
                    if main.ircprofiles[main.currentprofile][
                        "adminlist"][nick] == i[1]:
                            adminlevel = i[0]
            except KeyError:
                adminlevel = 0
            ct.msg(cmd.getname(nick) + ": Admin " + str(adminlevel))
        else:
            ct.commands.whois(ct.ircuser())
            ct.msg("Login attempt processed.")

    if ct.code("330")\
        and mp.text().find(":is logged in as") != -1:
            nick = ct.getsplit(3)
            auth = ct.getsplit(4)
            ct.profile.setauth(nick, auth)
            print(("Adding " + nick + " as " + auth))
    elif ct.code("307")\
        and (mp.text().find(":is identified for this nick") != -1 or
            mp.text().find(":is a registered nick") != -1 or
            mp.text().find(":has identified for this nick") != -1 or
            mp.text().find(":has identified for t\nhis nick") != -1):
            nick = ct.getsplit(3)
            auth = nick
            ct.profile.setauth(nick, auth)
            print(("Adding " + nick + " as " + auth))
    elif ct.code("311") and ct.profile.noauth():
        nick = ct.getsplit(3)
        auth = nick
        ct.profile.setauth(nick, auth)
        print(("Adding " + nick + " as " + auth + " with noauth"))

    if ct.code("353"):
        for i in ct.nameslist():
            n = i.strip('@+:')
            ch = ct.getsplit(4)
            main.nlistadd(n, ch)
            if getwlistlevel(n) > 0:
                main.whois(n)


def showhelp():
    main.sendcmsg(cmd.cprefix() + "login [-check]: Login to this bot as admin.")
    main.sendcmsg(
        "-check [<nick>]: Check if you/<nick> are logged in as admin.")
    main.sendcmsg(cmd.cprefix() + "wlist -set=<level> nick:" +
    "Add a nick to the whitelist, -set defaults to 0.")