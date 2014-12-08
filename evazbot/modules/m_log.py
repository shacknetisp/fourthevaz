# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from base import *
import datetime
import sys
import time
import os

dbfolder = c_redeclipse.dbhome + "/logs"
try:
  os.mkdir(dbfolder)
except:
  pass

def msg(mp):
        loc = mp.text().find(" :") + len(" :")
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        fout = "[" + st + "] " + "<" + mp.ircuser() + "> " + mp.text()[loc:]
        if len(mp.text()[loc:]) > 0:
            cname = main.getchannel()
            cname  = cname.replace("#","")
            if cname == main.ircprofiles[main.currentprofile]["nick"]:
                cname = main.getuser()
            with open(dbfolder + "/" + cname + ".channel", "a") as f:
                f.write(fout + "\n")

def output():
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        fout = "[" + st + "] " + "<" + main.ircprofiles[main.currentprofile]["nick"] + "> " + main.outputtext
        if len(main.outputtext) > 0:
            cname = main.outputchannel
            cname = cname.replace("#","")
            with open(dbfolder + "/" + cname + ".channel", "a") as f:
                f.write(fout + "\n")