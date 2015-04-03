# -*- coding: utf-8 -*-
import configs.mload
import utils
from . import utils as ircutils
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
        if user in self.server.whoislist:
            if 'done' in self.server.whoislist[user]:
                t = self.server.whoislist[user]
                authed = t['authed'] if 'authed' in t and t['authed'] else ''
        self.setaccess("%s:%s:%s" % (
            self.sp.sendernick, self.sp.host, authed))
        self.user = self.sp.sendernick

    def get_aliases(self):
        channeld = {}
        if self.channel:
            channeld = self.channel.aliases
        return utils.merge_dicts(self.server.aliasdb,
            channeld)

    def ltnserver(self):
        if 'ltnservers' in self.server.db:
            if self.sp.sendernick in self.server.db['ltnservers']:
                return True
        return False

    def setaccess(self, s=""):
        if s:
            self.accesslevelname = s
        c = (self.channel.entry['channel']
            if self.channel is not None else
            "")
        self.channellevel = self.server.get_channel_access(
            access.getaccesslevel, self,
            c)
        self.serverlevel = access.getaccesslevel(
            self.server, self.accesslevelname, "", self.channel)

    def isquery(self):
        return self.sp.target == self.server.nick

    def outtarget(self):
        if self.isquery():
            return self.sp.sendernick
        else:
            return self.sp.target

    def accesslevel(self):
        return max(
            self.serverlevel,
            self.channellevel)

    def channelaccess(self, channel):
        return max(self.server.get_channel_access(
            access.getaccesslevel, self,
            channel), self.serverlevel)

    def reply(self, message, c=''):
        if self.channel:
            if not self.server.db[
                'bot.enable.%s' % self.channel.entry['channel']]:
                return
        command = c
        if not command:
            if self.channel:
                command = 'PRIVMSG'
            else:
                command = 'NOTICE'
        self.server.do_base_hook('output', self, self.outtarget(), message)
        for m in message.split('\n'):
            self.server.write_cmd(command, self.outtarget() + str(' :') + m)

    def replyctcp(self, message):
        self.reply(ircutils.ctcp(message), "NOTICE")

    def replypriv(self, message, c=''):
        command = c
        if not command:
            if self.channel:
                command = 'PRIVMSG'
            else:
                command = 'NOTICE'
        self.server.do_base_hook('output', self, self.sp.sendernick, message)
        for m in message.split('\n'):
            self.server.write_cmd(command, self.sp.sendernick + str(' :') + m)

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
                    self.aliases = self.fp.server.db['aliases:%s' % (
                    c['channel'])]
                    return
            self.entry = None