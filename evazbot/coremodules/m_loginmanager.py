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


def get(ct):
    if ct.cmd("wlist"):
        try:
            level = int(ct.args.get("set"))
        except:
            main.sendcmsg("No argument!")
            return True
        if ct.args.getdef() == ct.user():
            ct.msg("You cannot set yourself.")
            return True
        if ct.islogin(level + 1) and (ct.getwlevel(mp.argsdef()) <
        ct.getwlevel(ct.user())):
            c_wlist.getcwlist()[mp.argsdef()] = level
            main.sendcmsg(cmd.getname(mp.argsdef()) +
            " is now at level " + str(level))
        else:
            main.sendcmsg("You can only set: 0 to " +
            str(ct.getwlevel(mp.user()) - 1))
            main.sendcmsg("The level of your target is: " +
            str(ct.getwlevel(mp.argsdef())))
        save()
    if ct.cmd("login"):
        if ct.args.getbool("check"):
            nick = ct.args.getdef().strip()
            if len(nick) == 0:
                nick = ct.user()
            wlistlevel = ct.getwlevel(nick)
            ct.msg(cmd.getname(nick) + ": Whitelist " + str(wlistlevel))
            adminlevel = ct.getalevel(nick)
            ct.msg(cmd.getname(nick) + ": Admin " + str(adminlevel))
        else:
            ct.commands.whois(ct.ircuser())
            ct.msg("Login attempt processed.")

    if ct.code("330")\
        and ct.text().find(":is logged in as") != -1:
            nick = ct.getsplit(3)
            auth = ct.getsplit(4)
            ct.profile.setauth(nick, auth)
            print(("Adding " + nick + " as " + auth))
    elif ct.code("307")\
        and (ct.text().find(":is identified for this nick") != -1 or
            ct.text().find(":is a registered nick") != -1 or
            ct.text().find(":has identified for this nick") != -1 or
            ct.text().find(":has identified for t\nhis nick") != -1):
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
            if ct.getwlevel(n) > 0:
                main.whois(n)


def showhelp(h):
    h("login [-check]: Login to this bot as admin.\n" +
    "-check [<nick>]: Check your/nick's login levels")
    h("wlist -set=<level> nick:" +
    "Add a nick to the whitelist, -set defaults to 0.")