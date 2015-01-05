# -*- coding: utf-8 -*-
import socket
import random
import time
from evazbot.configs import c_net
import select
import re
from collections import deque

running = True
channel = "nochannel"
random.seed()
currentuser = ""
outputtext = ""
outputchannel = ""
handled = False
wasserver = False
ircsocks = []
currentprofile = -1
adminlist = {}
ircprofiles = []
cwlist = {}
outputbuffer = deque()

exec(open("evazbot/configs/c_local/profiles.py").read())


def ircwrite(msg):
    global currentprofile
    outputbuffer.append((ircprofiles[currentprofile]["ircsock"],
        msg.encode('utf-8', 'ignore') + b"\n"))


def getchannel():
    return channel


def getuser():
    return currentuser


def sendmsg(chan, msg):
    import evazbot.configs.c_modules as c_modules
    global outputtext
    global outputchannel
    outputtext = msg
    outputchannel = chan
    c_modules.event("output")
    time.sleep(0.025)
    ircwrite("PRIVMSG " + chan + " :" + msg)


def sendcmsg(msg):
    if channel == ircprofiles[currentprofile]["nick"]:
        sendmsg(getuser(), msg)
    else:
        sendmsg(channel, msg)


def sendamsg(msg):
    global currentprofile
    for i in ircprofiles[currentprofile]["channels"]:
        sendmsg(i, msg)


def sendsmsg(chan, msg):
    if chan == "all":
        sendamsg(msg)
    else:
        sendmsg(chan, msg)


def joinchan(chan):
    ircwrite("JOIN " + chan)


def whois(n):
    ircwrite("WHOIS " + n)


def ircconnect():
    global currentprofile
    for i in range(len(ircprofiles)):
        currentprofile = i
        ircprofiles[currentprofile]["adminlist"] = dict()
        ircprofiles[currentprofile]["joined"] = False
        try:
            ircprofiles[currentprofile]["ircsock"].connect(
                (ircprofiles[currentprofile]["server"], 6667))
            ircwrite('USER %s 8 * :%s\r\n' % (
                ircprofiles[currentprofile]["nick"],
                ircprofiles[currentprofile]["nick"]))
            ircwrite("NICK " + ircprofiles[currentprofile]["nick"])
            time.sleep(0.25)
        except socket.error:
            pass


ircconnect()


def dochannel(ircmsg, i):
    global channel
    if ircmsg.find("PRIVMSG " + i + " :") != -1:
        channel = i
    if (
            ircmsg.endswith("JOIN " + i)
            or ircmsg.endswith("PART " + i)
            or ircmsg.find("PART " + i + " :") != -1
            or ircmsg.find("QUIT :") != -1
    ):
        channel = i


def process(ircmsgp):
    from evazbot.configs import u_commands as cmd
    import evazbot.configs.c_modules as c_modules
    global channel
    global currentuser
    global currentprofile
    ircmsg = ircmsgp
    ircmsg = ircmsg.strip('\n\r')
    if len(ircmsg) > 1:
        print(ircmsg)
        channel = "nochannel"
        if ircmsg.endswith(":+x") or ircmsg.endswith(":+i") or\
        ircmsg.endswith(":+ix"):
            ircprofiles[currentprofile]["joined"] = True
            for c in ircprofiles[currentprofile]["channels"]:
                joinchan(c)
            c_modules.event("joined")
        for i in ircprofiles[currentprofile]["channels"]:
            dochannel(ircmsg, i)
        dochannel(ircmsg, ircprofiles[currentprofile]["nick"])
        currentuser = cmd.getircuser(ircmsg)
        if ircmsg.find("PING :") == 0:
            c_modules.event("ping", ircmsg)
        elif ircmsg.find("ERROR :") == 0 and\
        ircmsg.find("Ping timeout :") != -1:
            pass
        elif ircmsg.find(":" + ircprofiles[currentprofile]["nick"] + "!") == 0\
        and ircmsg.find("JOIN") != -1:
            c_modules.event("login")
        else:
            global handled
            global wasserver
            handled = False
            wasserver = False
            c_modules.event("text", ircmsg)
            c_modules.event("msg", ircmsg)
            c_modules.event("afterall", ircmsg)


def loop_select():
    import evazbot.configs.c_modules as c_modules
    global channel
    global currentprofile
    lasttime = time.time()
    while running:
        sockets = []
        for p in range(len(ircprofiles)):
            sockets.append(ircprofiles[p]["ircsock"])
        selectresult, sr2, sr3 = select.select(sockets, [], [], 0.2)
        if time.time() - lasttime >= 1:
            lasttime = time.time()
            c_modules.event("tick")
        for socket in selectresult:
            for r in range(len(ircprofiles)):
                if ircprofiles[r]["ircsock"] == socket:
                    currentprofile = r
                    try:
                        ircmsg = ircprofiles[currentprofile][
                            "ircsock"].recv(4096).decode()
                        regex = re.compile(
                            "\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)
                        ircmsg = regex.sub("", ircmsg)
                    except socket.error as exc:
                        raise exc
                    msgs = ircmsg.split("\r\n")
                    for i in msgs:
                        process(i)
        linessent = 0
        for osock, output in outputbuffer:
            osock.send(output)
            linessent += 1
            time.sleep(0.025 * linessent)
        outputbuffer.clear()


def ircmain():
    import evazbot.configs.c_modules as c_modules
    c_modules.init()
    c_modules.load()
    print(("Starting " + c_net.name + "..."))
    c_modules.event("start")
    loop_select()
    c_modules.event("stop")
    for i in range(len(ircprofiles)):
        ircprofiles[i]["ircsock"].close()
