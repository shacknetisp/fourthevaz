# -*- coding: utf-8 -*-
import socket
import random
import time
import sys
from evazbot.configs import c_net
from evazbot.configs import c_locs
import select
from imp import reload
import re

running = True
channel = "nochannel"
random.seed()
currentuser = ""
outputtext = ""
outputchannel = ""
handled = False
ircsocks = []
currentprofile = -1

exec(open("evazbot/configs/c_local/profiles.py").read())


def ircwrite(msg):
    global currentprofile
    ircprofiles[currentprofile]["ircsock"].send(msg.encode('latin-1', 'ignore') + b"\n")


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


def ircconnect():
    global currentprofile
    for i in range(len(ircprofiles)):
        currentprofile = i
        try:
            ircprofiles[currentprofile]["ircsock"].connect((ircprofiles[currentprofile]["server"], 6667))
            ircwrite("USER " + ircprofiles[currentprofile]["nick"] + " " + ircprofiles[currentprofile]["nick"]
                     + " " + ircprofiles[currentprofile]["nick"] + " :" + ircprofiles[currentprofile]["name"])
            ircwrite("NICK " + ircprofiles[currentprofile]["nick"])
            for c in ircprofiles[currentprofile]["channels"]:
                joinchan(c)
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
            or ircmsg.endswith("PART " + i) or ircmsg.find("PART " + i + " :") != -1
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
        for i in ircprofiles[currentprofile]["channels"]:
            dochannel(ircmsg, i)
        dochannel(ircmsg, ircprofiles[currentprofile]["nick"])
        currentuser = cmd.getircuser(ircmsg)
        if ircmsg.find("PING :") == 0:
            c_modules.event("ping")
        elif ircmsg.find("ERROR :") == 0 and ircmsg.find("Ping timeout :") != -1:
            pass
        elif ircmsg.find(":" + ircprofiles[currentprofile]["nick"] + "!") == 0 and ircmsg.find("JOIN") != -1:
            c_modules.event("login")
        else:
            global handled
            handled = False
            c_modules.event("text", ircmsg)
            c_modules.event("msg", ircmsg)
            c_modules.event("afterall",ircmsg)


def loop():
    import evazbot.configs.c_modules as c_modules
    global channel
    global currentprofile
    lasttime = time.time()
    while running:
        poll = select.epoll()
        for p in range(len(ircprofiles)):
            poll.register(ircprofiles[p]["ircsock"], select.POLLIN)
        ready = poll.poll(0.2)
        time.sleep(0.1)
        if time.time() - lasttime >= 1:
            lasttime = time.time()
            c_modules.event("tick")
        for fd, flag in ready:
            for r in range(len(ircprofiles)):
                if ircprofiles[r]["ircsock"].fileno() == fd:
                    currentprofile = r
                    try:
                        ircmsg = ircprofiles[currentprofile]["ircsock"].recv(2048).decode()
                        regex = re.compile("\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)
                        ircmsg = regex.sub("",ircmsg)
                    except socket.error as exc:
                        raise exc
                    msgs = ircmsg.split("\r\n")
                    for i in msgs:
                        process(i)


def ircmain():
    import evazbot.configs.c_modules as c_modules
    c_modules.init()
    c_modules.load()
    print("Starting " + c_net.name + "...")
    c_modules.event("start")
    loop()
    c_modules.event("stop")
    for i in range(len(ircprofiles)):
        ircprofiles[i]["ircsock"].close()
