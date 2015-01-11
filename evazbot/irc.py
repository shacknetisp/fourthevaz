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

        def getdef(self, s='"\''):
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

    def write(self, command, message):
        main.ircwrite(command + ' ' + message)

    def msg(self, message, target='', command='PRIVMSG'):
        if target == '':
            target = main.getchannel()
        main.sendmsg(target, message, command)

    def user(self):
        return self.mp.user()

    def ircuser(self):
        return self.mp.ircuser()

    def getsplit(self, i):
        return self.mp.text().split()[i]

    def code(self, c):
        return self.mindex.code() == c

    def nameslist(self):
        return self.mp.text()[self.mp.text().index(":" + main.ircprofiles[
        main.currentprofile]["nick"]):].split()

    def islogin(self, w, a):
        if self.mp.iswlist(w):
            if self.mp.isadmin(a):
                return True
        return False


def getcontext(mp):
    return irccontext(mp)

