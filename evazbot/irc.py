# -*- coding: utf-8 -*-
from base import *


class irccontext:

    class mindex:

        def __init__(self, ct):
            self.ct = ct

        def sender(self):
            return self.ct.getsplit(0)

        def code(self):
            return self.ct.getsplit(1)

        def target(self):
            return self.ct.getsplit(2)

    class args:

        def __init__(self, ct):
            self.ct = ct

        def getdict(self):
            return self.ct.mp.argsn

        def getlist(self):
            return list(self.ct.mp.argsn.keys())

        def getdef(self, s=''):
            return self.ct.mp.argsdef(s)

        def getbool(self, arg):
            return self.ct.mp.argbool(arg)

        def get(self, arg, d=""):
            return self.ct.mp.argstr(arg, str(d))

    class commands:

        def __init__(self, ct):
            self.ct = ct

        def whois(self, nick):
            self.ct.write('WHOIS', nick)

        def join(self, channel):
            self.ct.write('JOIN', channel)

        def part(self, channel):
            self.ct.write('PART', channel)

    class profile:

        def __init__(self, ct):
            self.ct = ct

        def noauth(self):
            return 'noauth' in c_wlist.profiles[main.ircprofiles[
            main.currentprofile]['whitelist']] and c_wlist.getw('noauth')

        def setauth(self, nick, auth):
            main.ircprofiles[main.currentprofile]["adminlist"][nick] = auth

    def __init__(self, mp):
        self.mp = mp
        self.mindex = irccontext.mindex(self)
        self.profile = irccontext.profile(self)
        self.commands = irccontext.commands(self)
        self.args = irccontext.args(self)

    def cmd(self, name, wlevel=0, alevel=0):
        if(self.mp.cmd(name)):
            if self.mp.wcmd(name, wlevel):
                if self.mp.acmd(name, alevel):
                    return True
        return False

    def isserver(self):
        return self.mp.isserver()

    def write(self, command, message):
        main.ircwrite(command + ' ' + message)

    def msg(self, message, target='', command='PRIVMSG'):
        if target == '':
            main.sendcmsg(message, command)
        else:
            main.sendmsg(target, message, command)

    def channel(self):
        return self.mindex.target()

    def user(self):
        return self.mp.user()

    def botnick(self):
        return main.ircprofiles[main.currentprofile]["nick"]

    def botname(self):
        return main.botname()

    def isprivate(self):
        return self.mindex.target() == self.botnick()

    def ircuser(self):
        return self.mp.ircuser()

    def getsplit(self, i):
        try:
            return self.mp.text().split()[i]
        except IndexError:
            return ''

    def code(self, c):
        return self.mindex.code() == c

    def text(self):
        return self.mp.text()

    def nameslist(self):
        return self.mp.text()[self.mp.text().index(
            self.getsplit(4)) + len(self.getsplit(4)):].split()

    def islogin(self, w=0, a=0, message=False):
        if self.mp.iswlist(w):
            if self.mp.isadmin(a):
                return True
        if message:
            self.msg('You need level %d:%d.' % (w, a))
        return False

    def getwlevel(self, nick):
        wlistlevelc = 0
        wlistlevelmc = 0
        for name in c_wlist.getw("whitelist"):
            for n in name[1]:
                if nick == n:
                    wlistlevelc = name[0]
        try:
            wlistlevelmc = c_wlist.getcwlist()[nick]
        except KeyError:
            pass
        return max(wlistlevelc, wlistlevelmc)

    def getalevel(self, nick):
        try:
            for i in c_wlist.getw("adminlist"):
                if main.ircprofiles[main.currentprofile][
                    "adminlist"][nick] == i[1]:
                        if i[0] is None:
                            return 0
                        return i[0]
        except KeyError:
            return 0


def getcontext(mp):
    return irccontext(mp)


class dccconnection:
        def __init__(self, nick, ip, port, wlistlevel):
            import socket
            self.nick = nick
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.wlistlevel = wlistlevel
            self.socket.connect((ip, int(port)))
            self.profile = main.currentprofile

        def send(self, text):
            import evazbot.configs.c_modules as c_modules
            self.socket.send(text.encode('utf-8', 'ignore') + b"\n")
            c_modules.dccevent("dccout", self, text.strip())

        def sendbin(self, bint):
            import evazbot.configs.c_modules as c_modules
            self.socket.send(bint)
            c_modules.dccevent("dccout", self, text.strip())