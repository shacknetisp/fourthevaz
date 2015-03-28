# -*- coding: utf-8 -*-
import configs.mload
import utils
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
        self.channellevel = access.getaccesslevel(
            self.server, self.accesslevelname,
            str(self.server.entry[
                'settings'] + ':' + self.channel.entry['channel'])
            if self.channel is not None else
            "")
        self.serverlevel = access.getaccesslevel(
            self.server, self.accesslevelname)

    def get_aliases(self):
        channeld = {}
        if self.channel:
            channeld = self.channel.aliases
        return utils.merge_dicts(self.server.aliasdb,
            channeld)

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
                    self.aliases = self.fp.server.db.db['aliases:%s' % (
                    c['channel'])]
                    return
            self.entry = None