# -*- coding: utf-8 -*-
from base import *
import shlex

servernames = []


def cprefix():
    out = main.ircprofiles[main.currentprofile]["prefix"]
    if out.isalnum():
        raise ValueError('command prefix cannot be alphanumeric')
    return out

##mconfig/ucmd.py
##options:
#servernames.append('myreserver')


def umconfig(m):
    import evazbot.configs.c_locs as c_locs
    try:
        return open(c_locs.mconfigpath + "/" + m + ".py").read()
    except FileNotFoundError:
        return ""
exec(umconfig("ucmd"))


def isservername(name):
    if name in servernames:
        return True
    return False


def getuser(message):
    name = find_between(message, ":", "!")
    if message.find(name) != 1:
        name = "no_name"
    if isservername(name):
        name = find_between(message, ":<", "> ")
    return name


def getcmd(ircmsg, c, mark=cprefix()):
    if len(getuser(ircmsg).strip()) > 0:
        if ircmsg.find("PRIVMSG " + main.getchannel() + " :" + mark) != -1\
        or ircmsg.find(getuser(ircmsg) + "> " + mark) != -1:
            if (ircmsg.find(":" + mark + c + " ") != -1 or (
                    ircmsg.find(":" + mark + c) != -1
                    and ircmsg.endswith(":" + mark + c)) or ircmsg.find(
                    "> " + mark + c + " ") != -1 or (
                    ircmsg.find("> " + mark + c) != -1 and
                    ircmsg.endswith("> " + mark + c))):
                main.handled = True
                return True
    else:
        main.wasserver = True
    return False


def getcwlist(u):
    import evazbot.configs.c_wlist as c_wlist
    try:
        return c_wlist.getcwlist()[u]
    except KeyError:
        return 0


def iswlist(ircmsg, w=1):
    import evazbot.configs.c_wlist as c_wlist
    if w == 0:
        return True
    if getcwlist(getuser(ircmsg)) >= w:
        return True
    for name in c_wlist.getw("whitelist"):
        for n in name[1]:
            if name[0] >= w or name[0] == 999:
                if getuser(ircmsg) == n:
                    return True
    return False


def isadmin(ircmsg, w=1):
    import evazbot.configs.c_wlist as c_wlist
    if w == 0:
        return True
    try:
        for i in c_wlist.getw("adminlist"):
            if main.ircprofiles[main.currentprofile][
                "adminlist"][getuser(ircmsg)] == i[1] and i[0] >= w:
                return True
    except KeyError:
        return False
    return False


def getwcmd(ircmsg, c, w=1):
    if iswlist(ircmsg, w) and getcmd(ircmsg, c):
        return True
    if getcmd(ircmsg, c):
        main.sendcmsg("You are not authorized to preform this action.")
    return False


def getacmd(ircmsg, c, w=1):
    ok = False
    if isadmin(ircmsg, w):
        ok = True
    if ok:
        if getwcmd(ircmsg, c, w):
            return True
        else:
            return False
    elif getcmd(ircmsg, c):
        main.sendcmsg("You are not an admin!")
        return False
    return False


def getargs(msg, command):
    fcstring_i = " :" + cprefix() + command
    fcstring_g = "> " + cprefix() + command
    if msg.find(fcstring_i) != -1:
        loc = msg.find(fcstring_i) + len(fcstring_i) + 1
        args = msg[loc:]
    elif msg.find(fcstring_g) != -1:
        loc = msg.find(fcstring_g) + len(fcstring_g) + 1
        args = msg[loc:]
    else:
        args = ""
    return args
    return args


def getname(name, usenames=True):
    try:
        for i in c_wlist.getw("names"):
            for n in i[0]:
                if name == n and usenames:
                    return i[1]
        if name.find("@") != -1:
            return "[" + name[1] + "]" + name[2:]
        else:
            return "[" + name[0] + "]" + name[1:]
    except IndexError:
        return "no_name"


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def getircuser(message):
    name = find_between(message, ":", "!")
    if message.find(name) != 1:
        name = "no_name"
    return name


def outlist(l, n=6, delim="|"):
    text = ""
    addn = 0
    for i in l:
        text += i + " " + delim + " "
        addn += 1
        if addn >= n:
            main.sendcmsg(text)
            text = ""
            addn = 0
    if text:
        main.sendcmsg(text)


class MParser:
    def argsdef(self, s='"\''):
        if hasattr(self, "error"):
            raise self.error
        return self.argsdefv.strip(s)

    def argbool(self, arg):
        if not self.argsn:
            return False
        return arg in self.argsn

    def argstr(self, arg, d=""):
        if self.argbool(arg):
            return self.argsn[arg]
        else:
            return d

    def basecmd(self, c):
        self.argsn = self._argsn(c)

    def text(self):
        return self.message

    def user(self):
        return getuser(self.message)

    def ircuser(self):
        return getircuser(self.message)

    def userf(self):
        return getname(self.user())

    def cmd(self, c):
        self.basecmd(c)
        return getcmd(self.message, c)

    def wcmd(self, c, w=1):
        self.basecmd(c)
        return getwcmd(self.message, c, w)

    def iswlist(self, w=1):
        return iswlist(self.message, w)

    def isadmin(self, w=1):
        return isadmin(self.message, w)

    def acmd(self, c, w=1):
        self.basecmd(c)
        return getacmd(self.message, c, w)

    def code(self, i):
        try:
            c = self.text().split(' ')[1]
        except:
            c = ""
        return c == i

    def args(self, c=""):
        return self.argsv

    def _argsn(self, c):
        self.argsv = getargs(self.message, c)
        lastval = ""
        ret = {}
        self.argsdefv = ""
        ar = []
        try:
            ar = shlex.split(self.args(c))
        except ValueError as e:
            self.error = e
        ok = True
        for i in ar:
            if i[0] == '-' and ok:
                var = i.split("=")[0][1:]
                try:
                    val = i.split("=")[1]
                except:
                    val = ""
                ret[var] = val
                lastval = i
            else:
                ok = False
        lastval = lastval.strip()
        if lastval:
            self.argsdefv = self.args(c)[
              self.args(c).rfind(lastval) + len(lastval):]
            self.argsdefv = self.argsdefv[self.argsdefv.find('" ') + 2:]
        else:
            self.argsdefv = self.args(c)
        return ret

    def isserver(self):
        name = find_between(self.message, ":", "!")
        return isservername(name)

    def isjp(self, m):
        for i in main.ircprofiles[main.currentprofile]["channels"]:
            if self.message.find(m + " " + i + " :") != -1 or\
            self.message.endswith(m + " " + i):
                return True
        return False

    def isquit(self):
        for i in main.ircprofiles[main.currentprofile]["channels"]:
            if self.message.find("QUIT :") != -1:
                return True
        return False

    def __init__(self, p_message):
        self.message = p_message
