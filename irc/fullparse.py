# -*- coding: utf-8 -*-
import base.fullparse
import textwrap
from . import utils as ircutils
formatcodes = ircutils.formatcodes


class FullParse(base.fullparse.FullParse):

    def __init__(self, server, sp, dcc=None, nomore=None):
        super(FullParse, self).__init__(server, nomore=nomore)
        self.sp = sp
        """SplitParser object."""
        self.dcc = dcc
        """DCC object, set to None if the message didn't come from DCC."""
        self.channel = None
        """A FullParse.Channel object, set to None if not in a channel."""
        authed = ""
        self.user = self.sp.sendernick
        """
        IRC Nick or name from an external server (Red Eclipse, etc...).
        Use unless you need to directly get the IRC nick.
        """
        if self.user in self.server.whoislist:
            if 'done' in self.server.whoislist[self.user]:
                t = self.server.whoislist[self.user]
                authed = t['authed'] if 'authed' in t and t['authed'] else ''
        self.setaccess("%s=%s=%s" % (
            self.sp.sendernick, self.sp.host, authed))
        if self.isquery() or self.sp.target == '*':
            self.channel = None
        else:
            self.channel = FullParse.Channel(self)
            if not self.channel.entry:
                self.channel = None
        o = {'external': False}
        self.server.do_base_hook('isexternal', self, o)
        self.isexternal = o['external']

    def get_aliases(self):
        """Returns a dictionary of all current aliases."""
        channeld = {}
        if self.channel:
            channeld = self.channel.aliases
        return utils.merge_dicts(self.server.aliasdb,
            channeld)

    def hasright(self, right):
        """Returns if the user has the specified right."""
        access = self.server.import_module('rights.access', False)
        extra = []
        for c in self.server.channels:
            extra += self.channelrights(self.sp.sendernick, c)
        return (right in (access.fullrights(self, access.getrights(
            self.server, self.accesslevelname) + extra)))

    def isquery(self):
        """Did the message come from a query?"""
        return self.sp.target == self.server.nick

    def me(self, text):
        """Returns an ACTION text"""
        return '\x01ACTION %s\x01' % text

    def outtarget(self):
        """Returns the target to send messages to."""
        if self.isquery():
            return self.sp.sendernick
        else:
            return self.sp.target

    def channelrights(self, nick, channel):
        extra = []
        if not self.external() and channel:
            if nick in self.server.whoislist:
                if 'names' not in channel or nick not in channel['names']:
                        return extra
                if channel[
                    'channel'] in self.server.whoislist[
                        nick]['op']:
                        extra.append('%s,op' % channel['channel'])
                if channel[
                    'channel'] in self.server.whoislist[
                        nick]['voice']:
                        extra.append('%s,voice' % channel['channel'])
        return extra

    def haschannelright(self, right):
        """Returns if the user has the specified channel right."""
        access = self.server.import_module('rights.access', False)
        right = (self.channel.entry[
            'channel'] if self.channel else '') + ',' + right
        return (right in access.fullrights(self, access.getrights(
            self.server, self.accesslevelname) + self.channelrights(
                self.sp.sendernick,
                self.channel.entry if self.channel else None)))

    def channelhasright(self, right):
        """Returns if the channel has the specified right."""
        if not self.channel:
            return []
        access = self.server.import_module('rights.access', False)
        return (right in (access.getrights(self.server, self.channel.entry[
            'channel'])))

    def reply_driver(self, target, message, c=''):
        """Send <message> to <target> using <c> or the default."""
        if not message:
            return
        message = message.strip(' \n\t')
        command = c
        if not command:
            if self.channel:
                command = 'PRIVMSG'
            else:
                command = 'NOTICE'
        if message.count('\n') == 0 and not self.nomore:
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
        if self.dcc:
            self.server.do_base_hook('output', self,
                'dcc:' + self.dcc.nick, message)
        else:
            self.server.do_base_hook('output', self,
                target, message)
        for tm in message.split('\n'):
            i = 0
            for fm in textwrap.wrap(tm, 450):
                if self.external():
                    fm = fm.replace(formatcodes.bold, '')
                if self.dcc:
                    self.dcc.socket.send(
                        str(fm).encode() +
                    b'\n')
                else:
                    self.server.write_cmd(command, target + str(' :') +
                    ('...' if i else '') + fm)
                i += 1

    def reply(self, message, c=''):
        """Default reply function, reply with <message> [command <c>]."""
        if self.channelhasright('disable'):
            return
        return self.reply_driver(self.outtarget(), message, c)

    def replyctcp(self, message):
        """Reply with CTCP markers."""
        self.reply(ircutils.ctcp(message), "NOTICE")

    def sendctcp(self, message):
        """Send with CTCP markers."""
        self.reply(ircutils.ctcp(message), "PRIVMSG")

    def replypriv(self, message, c=''):
        """Reply using a query, ignore channels."""
        return self.reply_driver(self.sp.sendernick, message, c)

    def canuse(self, module, command=''):
        """Return if the user can use <module>[.<command>]"""
        for r in [':' + module,
            ':' + module + '.' + command]:
                dr = '-' + r
                if self.channelhasright(dr) and not self.hasright(
                    r):
                    return False
                if self.hasright(dr):
                    return False
                if self.haschannelright(dr) and not self.hasright(
                    r) and not self.haschannelright('op'):
                    return False
        return True

    class Channel:

        def __init__(self, fp, name=""):
            self.fp = fp
            self.name = ""
            self.findname(name)

        def findname(self, name=""):
            self.aliases = None
            '''Channel aliases reference.'''
            if not name:
                name = self.fp.sp.target
            for c in self.fp.server.channels:
                if name == c['channel']:
                    self.entry = c
                    self.name = name
                    self.aliases = self.fp.server.db['aliases:%s' % (
                    c['channel'])]
                    return
            self.entry = None
            """
            Entry in the server.
            Always contains:
            'channel': Channel name
            Probably contains:
            'names': List of nicks
            """