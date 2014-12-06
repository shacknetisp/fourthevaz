# -*- coding: utf-8 -*-
"""
def getncmd(ircmsg,cmd):
  global currentuser
  if ( ircmsg.find(":."+cmd) != -1) or (ircmsg.find("> ."+cmd) != -1):
      return 1
  return 0

def getcmd(ircmsg,cmd):
  global currentuser
  for name in (wlist.whitelist):
    if ( ircmsg.find(":."+cmd) != -1 and ircmsg.find(name+"!") != -1) or ircmsg.find(name+"> ."+cmd) != -1:
      currentuser=name
      return 1
  return 0
"""
from base import *

import shlex

def getuser(message):
    name = find_between(message, ":", "!")
    if message.find(name) != 1:
        name = "no_name"
    if name.find("snisp") == 0 or name.find("eleptor") == 0 or name.find("altre") == 0:
        name = find_between(message, ":<", "> ")
    return name

def getcmd(ircmsg, c):
    if ircmsg.find("PRIVMSG "+main.getchannel()+" :.") != -1 or ircmsg.find(getuser(ircmsg)+"> .") != -1:
        if (ircmsg.find(":." + c + " ") != -1 or (
                ircmsg.find(":." + c) != -1 and ircmsg.endswith(":." + c)) or ircmsg.find(
                "> ." + c + " ") != -1 or (
                ircmsg.find("> ." + c) != -1 and ircmsg.endswith("> ." + c))):
            main.handled = True
            return True
    return False


def getwcmd(ircmsg, c, w = 1):
    for name in c_wlist.whitelist:
        for n in name[1]:
            if name[0] >= w or name[0] == 999:
                if getuser(ircmsg) == n and getcmd(ircmsg,c):
                    return True
    if getcmd(ircmsg, c):
        main.sendcmsg("You are not authorized to preform this action.")
    return False


def getacmd(ircmsg, c, w = 1):
    ok = False
    for i in c_wlist.adminlist:
        if ircmsg.find(i[1]) == 0 and i[0] >= w:
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
    fcstring_i = " :." + command
    fcstring_g = "> ." + command
    if msg.find(fcstring_i) != -1:
      loc = msg.find(fcstring_i) + len(fcstring_i) + 1
      args = msg[loc:]
    elif msg.find(fcstring_g) != -1:
      loc = msg.find(fcstring_g) + len(fcstring_g) + 1
      args = msg[loc:]
    else:
      args=""
    return args


def getname(name):
  try:
    for i in c_wlist.names:
        for n in i[0]:
            if name == n:
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


def outlist(l, n=6, delim = "|"):
    text = ""
    addn = 0
    for i in l:
        text += i + " "+delim+" "
        addn += 1
        if addn >= n:
            main.sendcmsg(text)
            text = ""
            addn = 0
    if text:
        main.sendcmsg(text)


class MParser:
    def argsdef(self):
      if hasattr(self, "error"):
        raise self.error
      return self.argsdefv.strip('"\'')

    def argbool(self, arg):
        if not self.argsn:
            return False
        return arg in self.argsn

    def argstr(self, arg, d=""):
        if self.argbool(arg):
            return self.argsn[arg]
        else:
            return d

    def basecmd(self,c):
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

    def wcmd(self, c, w = 1):
        self.basecmd(c)
        return getwcmd(self.message, c, w)

    def acmd(self, c, w = 1):
        self.basecmd(c)
        return getacmd(self.message, c, w)

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
          self.error=e
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
          self.argsdefv = self.args(c)[self.args(c).rfind(lastval) + len(lastval) + 1:]
        else:
          self.argsdefv = self.args(c)
        return ret

    def isserver(self):
        name = find_between(self.message, ":", "!")
        return name.find("snisp") != -1 or name.find("eleptor") != -1

    def isjp(self, m):
        for i in main.ircprofiles[main.currentprofile]["channels"]:
            if self.message.find(m + " " + i + " :") != -1 or self.message.endswith(m + " " + i):
                return True
        return False

    def isquit(self):
        for i in main.ircprofiles[main.currentprofile]["channels"]:
            if self.message.find("QUIT :") != -1:
                return True
        return False

    def __init__(self, p_message):
        self.message = p_message
