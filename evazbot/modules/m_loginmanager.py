# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from base import *

def msg(mp):
  if mp.cmd("login"):
    main.whois(mp.ircuser())
    main.sendcmsg("Login attempt processed.")
  if mp.text().find("330") != -1 and mp.text().find(":is logged in as") != -1:
    nick = cmd.find_between(mp.text()," ",":is logged in as").split()[2]
    auth = cmd.find_between(mp.text()," ",":is logged in as").split()[3]
    main.adminlist[nick]=auth
    print("Adding "+nick+" as "+auth)
  if mp.text().find("353 "+main.ircprofiles[main.currentprofile]["nick"]) != -1:
    for i in mp.text().split():
      main.whois(i.strip("@"))

def showhelp():
    main.sendcmsg(".login: Check your nick to the admin list.")