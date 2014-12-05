# -*- coding: utf-8 -*-
from base import *
import urllib.request
import os

modname = "Core"


def start():
    c_wlist.load()


def msg(mp):
    if mp.acmd("reload", 999):
        main.sendamsg("Restarting...")
        monitor.addline("./restart ircbot")
        return True

    if mp.acmd("mreload"):
        reload(c_modules)
        reload(c_wlist)
        c_modules.reloadall()
        return True

    if mp.acmd("remove", 99):
        args = mp.args()
        splitargs = args.split()
        if len(splitargs) == 1:
            r = c_modules.remove(splitargs[0])
            if not r:
                main.sendcmsg("Couldn't remove module!");
        else:
            main.sendcmsg("Invalid Arguments!")
        return True
    if mp.acmd("add"):
        args = mp.args()
        splitargs = args.split()
        if len(splitargs) == 1:
            c_modules.astart(splitargs[0])
        else:
            main.sendcmsg("Invalid Arguments!")
        return True
    if mp.acmd("dadd", 99):
        args = mp.args()
        splitargs = args.split()
        if len(splitargs) == 1:
            lines = []
            for line in open(c_modules.dbfile, "r"):
                if line.split() != splitargs[0].split():
                    lines.append(line)
            lines.append(splitargs[0])
            lines.append("\n")
            with open(c_modules.dbfile, "w") as f:
                f.writelines(lines)
            c_modules.astart(splitargs[0])
            c_modules.reloadall()
        return True
    if mp.acmd("dremove", 99):
        args = mp.args()
        splitargs = args.split()
        if len(splitargs) == 1:
            lines = []
            try:
              for line in open(c_modules.dbfile, "r"):
                if line.split() != splitargs[0].split():
                    lines.append(line)
            except FileNotFoundError:
              main.sendcmsg("Module does not exist!")
              return True
            r = c_modules.remove(splitargs[0])
            if not r:
                main.sendcmsg("Module does not exist!");
            else:
                c_modules.reloadall()
        else:
            main.sendcmsg("Invalid Arguments!")
        return True
    if mp.wcmd("pend",99):
       name = mp.argsdef()
       import urllib.request, urllib.parse, urllib.error
       url = 'http://www.ghostclanre.tk/4e/mc_' + name + ".py"
       try:
         urllib.request.urlretrieve(url, c_redeclipse.cmpath + '/pending/mc_' + name + ".py")
         main.sendcmsg("Success! Ask a level 1000 admin for confirmation.")
       except ValueError:
         main.sendcmsg("Couldn't get module.")
       except IOError:
         main.sendcmsg("Couldn't get module.")
    if mp.acmd("confirm", 1000):
      name = mp.argsdef()
      fromf = c_redeclipse.cmpath + '/pending/mc_' + name + ".py"
      tof =  c_redeclipse.cmpath + '/mc_' + name + ".py"
      import shutil
      try:
        shutil.copyfile(fromf, tof)
        main.sendcmsg("Confirmed.");
      except IOError:
        main.sendcmsg("Pending Module not Found!")
    return False
    
    
def showhelp():
    main.sendcmsg(".reload: Relaunch " + c_net.name + ".")
    main.sendcmsg(".mreload: Stop modules & reload default modules.")
    main.sendcmsg(".wreload: Reload whitelists")
    main.sendcmsg(".add <m>: Load & start module <m>. If <m> is running, stop it.")
    main.sendcmsg(".remove <m>: Unload module <m>.")
    main.sendcmsg(".dadd <m>: Add module to the defaults list.")
    main.sendcmsg(".dremove <m>: Remove module from the defaults list.")
    main.sendcmsg(".confirm <m>: Move <m> from pending to active.");
    main.sendcmsg(".pend <m>: Copy <m> from online repository to pending.");

whitelistreload = 0;
def tick():
    global whitelistreload
    whitelistreload += 1
    if whitelistreload >= 5:
        reload(c_wlist)
        whitelistreload = 0