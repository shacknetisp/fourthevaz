# -*- coding: utf-8 -*-
import socket
import random
import time
from evazbot.configs import c_net
from evazbot.configs import c_variables as c_vars
from evazbot.configs import c_locs
import select
import re
from collections import deque
import sys
from string import Template

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
sys.path.append('deps')
aliasdb = c_vars.variablestore(c_locs.dbhome + "/alias.db.pkl")
try:
    aliasdb.load()
except:
    pass
exec(open("evazbot/configs/profiles.py").read())
for i in range(len(ircprofiles)):
    if 'prefix' not in ircprofiles[i]:
        ircprofiles[i]['prefix'] = '.'
    ircprofiles[i]['nicklist'] = {}
    ircprofiles[i]['channelnames'] = {}
    ircprofiles[i]['userinfo'] = {}
    ircprofiles[i]['whoisqueue'] = deque()
    ircprofiles[i]['lastwhois'] = 0
    for ch in ircprofiles[i]['channels']:
        ircprofiles[i]['channelnames'][ch] = []


def nlistcheck(n):
    if not n in ircprofiles[currentprofile]["nicklist"]:
        ircprofiles[currentprofile]["nicklist"][n] = []


def nlistadd(n, ch):
    nlistcheck(n)
    ircprofiles[currentprofile]["nicklist"][n].append(ch)


def botname():
    global currentprofile
    return ircprofiles[currentprofile]["name"]


def ircwrite(msg):
    global currentprofile
    outputbuffer.append((ircprofiles[currentprofile]["ircsock"],
        msg.encode('utf-8', 'ignore') + b"\n"))


def getchannel():
    return channel


def getuser():
    return currentuser


def sendmsg(chan, msg, t="PRIVMSG"):
    import evazbot.configs.c_modules as c_modules
    global outputtext
    global outputchannel
    for i in msg.split('\n'):
        outputtext = i
        outputchannel = chan
        c_modules.event("output")
        out = t + " " + chan + " :" + i
        ircwrite(out)
        print(out)


def sendcmsg(msg, t="PRIVMSG"):
    if channel == ircprofiles[currentprofile]["nick"]:
        sendmsg(getuser(), msg, t)
    else:
        sendmsg(channel, msg, t)


def sendhmsg(msg):
    import evazbot.configs.u_commands as cmd
    sendcmsg(cmd.cprefix() + msg)


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


def pconnect():
    global currentprofile
    ircprofiles[currentprofile]["adminlist"] = dict()
    ircprofiles[currentprofile]["joined"] = False
    try:
        ircprofiles[currentprofile]["ircsock"].connect(
            (ircprofiles[currentprofile]["server"], 6667))
        ircwrite('USER %s 8 * :%s' % (
            ircprofiles[currentprofile]["nick"],
            botname()))
        ircwrite("NICK " + ircprofiles[currentprofile]["nick"])
        time.sleep(0.25)
    except OSError:
        pass


def ircconnect():
    global currentprofile
    for i in range(len(ircprofiles)):
        currentprofile = i
        pconnect()


def dochannel(ircmsg, i):
    global channel
    global currentprofile
    from evazbot.configs import u_commands as cmd
    if ircmsg.find("PRIVMSG " + i + " :") != -1:
        channel = i
    if (
            ircmsg.endswith("JOIN " + i)
            or ircmsg.endswith("PART " + i)
            or ircmsg.find("PART " + i + " :") != -1
            or ircmsg.find("QUIT :") != -1
    ):
        channel = i
    try:
        if ircmsg.split()[1] == 'QUIT':
            if i in ircprofiles[
                currentprofile]['nicklist'][cmd.getircuser(ircmsg)]:
                channel = i
    except IndexError:
        pass
    except KeyError:
        pass


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
        elif ircmsg.find("ERROR :") == 0:
            ircprofiles[currentprofile]["ircsock"].close()
            pconnect()
        elif ircmsg.find(":" + ircprofiles[currentprofile]["nick"] + "!") == 0\
        and ircmsg.find("JOIN") != -1:
            c_modules.event("login")
        else:
            global handled
            global wasserver
            handled = False
            wasserver = False
            oldircmsg = ircmsg
            irt = Template(ircmsg)
            ircmsg = irt.safe_substitute(aliasdb.data_dict)
            if ircmsg != oldircmsg:
                print(('--' + ircmsg))
            c_modules.event("msg", ircmsg)
            c_modules.event("get", ircmsg)
            c_modules.event("afterall", ircmsg)
            c_modules.event("getafter", ircmsg)


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
            ocp = currentprofile
            for i in range(len(ircprofiles)):
                currentprofile = i
                c_modules.event("tick_profile")
            currentprofile = ocp
        got = False
        for csocket in selectresult:
            for r in range(len(ircprofiles)):
                if ircprofiles[r]["ircsock"] == csocket:
                    got = True
                    currentprofile = r
                    ircmsg = ""
                    try:
                        try:
                            ircmsg = ircprofiles[currentprofile][
                            "ircsock"].recv(4096).decode()
                        except UnicodeDecodeError:
                            pass
                        regex = re.compile(
                            "\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)
                        ircmsg = regex.sub("", ircmsg)
                    except OSError:
                        pconnect()
                    msgs = ircmsg.split("\r\n")
                    for i in msgs:
                        process(i)
        if not got:
            time.sleep(0.2)
        linessent = 0
        try:
            while outputbuffer:
                osock, output = outputbuffer.popleft()
                osock.send(output)
                linessent += 1
                time.sleep(0.025 * linessent)
                if linessent > 5:
                    time.sleep(0.05 * linessent)
                if linessent > 10:
                    break
        except IndexError:
            pass
        for i in range(len(ircprofiles)):
            currentprofile = i
            if ircprofiles[currentprofile]["whoisqueue"]:
                if (time.time() - ircprofiles[
                    currentprofile]["lastwhois"]) > 1.5:
                    ircprofiles[currentprofile]["lastwhois"] = time.time()
                    o = ircprofiles[currentprofile]["whoisqueue"].popleft()
                    if o in ircprofiles[currentprofile]['userinfo']:
                        ircprofiles[currentprofile][
                            'userinfo'][o]['offline'] = True
                    whois(o)


def safemkdir(d):
    import os
    if not os.path.isdir(d):
        os.mkdir(d)


def ircmain():
    import evazbot.configs.c_locs as c_locs
    print(("Database home is: " + c_locs.dbhome))
    safemkdir(c_locs.dbhome)
    safemkdir(c_locs.mconfigpath)
    import evazbot.configs.c_modules as c_modules
    c_modules.init()
    c_modules.load()
    ircconnect()
    print(("Starting " + c_net.name + "..."))
    c_modules.event("start")
    loop_select()
    c_modules.event("stop")
    for i in range(len(ircprofiles)):
        ircprofiles[i]["ircsock"].close()
