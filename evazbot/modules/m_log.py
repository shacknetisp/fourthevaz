# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from base import *
import datetime
import sys
import time

dbfolder = c_redeclipse.dbhome + "/logs"


def msg(mp):
        loc = mp.text().find(" :") + len(" :")
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        fout = "[" + st + "] " + "<" + mp.ircuser() + "> " + mp.text()[loc:]
        if len(mp.text()[loc:]) > 0:
            cname = main.getchannel()
            if cname[0] == '#':
                cname = cname[1:]
            elif cname == c_net.nick:
                cname = main.getuser()
            with open(dbfolder + "/" + cname + ".channel", "a") as f:
                f.write(fout + "\n")

def output():
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        fout = "[" + st + "] " + "<" + c_net.nick + "> " + main.outputtext
        if len(main.outputtext) > 0:
            cname = main.outputchannel
            if cname[0] == '#':
                cname = cname[1:]
            with open(dbfolder + "/" + cname + ".channel", "a") as f:
                f.write(fout + "\n")