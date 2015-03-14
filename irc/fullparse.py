# -*- coding: utf-8 -*-
import configs.mload
access = configs.mload.import_module_py('rights.access')


class FullParse():

    def __init__(self, server, sp):
        self.server = server
        self.sp = sp
        if self.isquery() or self.sp.target == '*':
            self.channel = None
        else:
            self.channel = FullParse.Channel(self)
            if not self.channel.entry:
                self.channel = None
        authed = ""
        user = self.sp.sendernick
        if user in self.server.whoislist and 'done' in self.server.whoislist[
            user]:
            t = self.server.whoislist[user]
            authed = t['authed'] if 'authed' in t and t['authed'] else ''
        self.accesslevelname = "%s:%s:%s" % (
            self.sp.sendernick, self.sp.host, authed)

    def isquery(self):
        return self.sp.target == self.server.nick

    def outtarget(self):
        if self.isquery():
            return self.sp.sendernick
        else:
            return self.sp.target

    def accesslevel(self):
        return access.getaccesslevel(self.server, self.accesslevelname)

    def reply(self, message, command='PRIVMSG'):
        self.server.write_cmd(command, self.outtarget() + str(' :') + message)

    class Channel:

        def __init__(self, fp, name=""):
            self.fp = fp
            self.findname(name)

        def findname(self, name=""):
            if not name:
                name = self.fp.sp.target
            for c in self.fp.server.channels:
                if name == c['channel']:
                    self.entry = c
                    return
            self.entry = None