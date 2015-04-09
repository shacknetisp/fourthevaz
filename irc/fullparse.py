# -*- coding: utf-8 -*-
import configs.mload
import utils
import textwrap
from . import utils as ircutils
formatcodes = ircutils.formatcodes
access = configs.mload.import_module_py('rights.access')


class FullParse():

    def __init__(self, server, sp):
        self.server = server
        self.sp = sp
        self.moreflag = False
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
        self.setaccess("%s=%s=%s" % (
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
            c, ltn=self.ltnserver())
        self.serverlevel = access.getaccesslevel(
            self.server, self.accesslevelname, "", self.channel,
            ltn=self.ltnserver())

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

    def reply_driver(self, target, message, c=''):
        if not message:
            return
        message = message.strip(' \n\t')
        command = c
        if not command:
            if self.channel:
                command = 'PRIVMSG'
            else:
                command = 'NOTICE'
        if message.count('\n') == 0:
            if self.moreflag:
                messages = textwrap.wrap(message, 450)
                self.moreflag = False
            else:
                messages = textwrap.wrap(message, 400)
            message = messages[0]
            if len(messages) > 1:
                self.server.state[
                    'more.%s' % self.user] = messages[1:]
                try:
                    if self.server.state['more.%s' % self.user]:
                        l = len(
                            self.server.state['more.%s' % self.user])
                        message += (' ' + formatcodes.bold +
                            '(%d more message%s)' % (l,
                            's' if l != 1 else ''))
                except KeyError:
                    pass
        self.server.do_base_hook('output', self, target, message)
        for tm in message.split('\n'):
            i = 0
            for fm in textwrap.wrap(tm, 450):
                if self.ltnserver():
                    fm = fm.replace(formatcodes.bold, '')
                self.server.write_cmd(command, target + str(' :') +
                ('...' if i else '') + fm)
                i += 1

    def reply(self, message, c=''):
        if self.channel:
            if not self.server.db[
                'bot.enable.%s' % self.channel.entry['channel']]:
                return
        return self.reply_driver(self.outtarget(), message, c)

    def replyctcp(self, message):
        self.reply(ircutils.ctcp(message), "NOTICE")

    def replypriv(self, message, c=''):
        return self.reply_driver(self.sp.sendernick, message, c)

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