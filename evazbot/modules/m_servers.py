# -*- coding: utf-8 -*-
#Beha's Servers Only!!!
from base import *

downdelay = 3 * 60
downmessagetime = 90
downto = 0
goingdown = False

downmsg = c_net.name + " and Beha's servers will go down, save your data. Minutes until shutdown: "


def msg(mp):
    global goingdown
    global downto
    global down30
    global downmessagetime
    if mp.acmd("servers", 999):
        args = mp.args()
        splitargs = args.split()
        if len(splitargs) == 1:
            if splitargs[0] == "restartall":
                monitor.addline("./servers")
            elif splitargs[0] == "down":
                goingdown = True
                downto = 0
            elif splitargs[0] == "cdown":
                main.sendamsg("Shutdown of servers cancelled.")
                down30 = downmessagetime
                goingdown = False
            elif splitargs[0] == "help":
                main.sendcmsg("Use .servers <command>")
                main.sendcmsg("restartall: Restart all servers and " + c_net.name + ".")
                main.sendcmsg("stop <server>: Stop <server>.")
                time.sleep(0.25)
                main.sendcmsg(
                    "restart <server> OR start <server>: Restart or Start server, depending on current state.")
                main.sendcmsg("down: Shutdown servers after a " + str(downdelay / 60) + " minute wait.")
                main.sendcmsg("cdown: Cancel pending shutdown.")
            else:
                main.sendcmsg("Invalid Arguments!")
        elif len(splitargs) == 2:
            if splitargs[0] == "stop":
                if splitargs[1] != "mon":
                    monitor.addline("./stop " + splitargs[1])
                    main.sendcmsg("Stopping " + splitargs[1])
            elif splitargs[0] == "restart" or splitargs[0] == "start":
                if splitargs[1] != "mon":
                    monitor.addline("./restart " + splitargs[1])
                    main.sendcmsg("Starting " + splitargs[1])
            else:
                main.sendcmsg("Invalid Arguments!")
        else:
            main.sendcmsg("Invalid Arguments!")
        return True
    return False


def showhelp():
    time.sleep(0.25)
    main.sendcmsg(".servers help: All .server commands.")


down30 = downmessagetime


def tick():
    global downto
    global down30
    global goingdown
    global downmessagetime
    if goingdown:
        print(downto)
        downto += 1
        down30 += 1
        if down30 > downmessagetime:
            mdir = str(round((downdelay * 1.0 - downto * 1.0) / 60.0, 2))
            main.sendamsg(downmsg + mdir)
            down30 = 0
        if downto >= downdelay:
            main.sendamsg("The servers will now shutdown within 10 seconds. Adieu!")
            main.sendamsg("This is Fourth Evaz, signing off.")
            monitor.addline("killall redeclipse_server && killall ib && ./stop mon")
            goingdown = False
