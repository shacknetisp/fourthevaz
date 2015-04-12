# -*- coding: utf-8 -*-
import utils
import textwrap
from . import utils as ircutils
formatcodes = ircutils.formatcodes


class FullParse():
    """High-level parser, contains Server and SplitParse references."""

    def __init__(self, server, sp):
        self.server = server
        self.isexternal = False
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
        o = {'external': False}
        self.server.do_base_hook('isexternal', self, o)
        self.isexternal = o['external']

    def me(self, text):
        """Returns an ACTION text"""
        return '\x01ACTION %s\x01' % text

    def get_aliases(self):
        """Returns a dictionary of all current aliases."""
        channeld = {}
        if self.channel:
            channeld = self.channel.aliases
        return utils.merge_dicts(self.server.aliasdb,
            channeld)

    def external(self):
        """Returns true if the messages comes from a server relay."""
        return self.isexternal

    def setaccess(self, s=""):
        """Set the access string of this fullparse object."""
        if s:
            self.accesslevelname = s

    def isquery(self):
        """Did the message come from a query?"""
        return self.sp.target == self.server.nick

    def outtarget(self):
        """Returns the target to send messages to."""
        if self.isquery():
            return self.sp.sendernick
        else:
            return self.sp.target

    def hasright(self, right):
        """Returns if the user has the specified right."""
        access = self.server.import_module('rights.access', False)
        extra = []
        for c in self.server.channels:
            extra += self.channelrights(c)
        return (right in (access.getrights(
            self.server, self.accesslevelname) + extra))

    def channelrights(self, channel):
        extra = []
        if not self.external() and channel:
            if self.sp.sendernick in self.server.whoislist:
                if channel[
                    'channel'] in self.server.whoislist[
                        self.sp.sendernick]['op']:
                        extra.append('%s,op' % channel['channel'])
                if channel[
                    'channel'] in self.server.whoislist[
                        self.sp.sendernick]['voice']:
                        extra.append('%s,voice' % channel['channel'])
        return extra

    def haschannelright(self, right):
        """Returns if the user has the specified channel right."""
        access = self.server.import_module('rights.access', False)
        right = (self.channel.entry[
            'channel'] if self.channel else '') + ',' + right
        return (right in access.getrights(
            self.server, self.accesslevelname) + self.channelrights(
                self.channel.entry if self.channel else None))

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
                if self.external():
                    fm = fm.replace(formatcodes.bold, '')
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

    def replypriv(self, message, c=''):
        """Reply using a query, ignore channels."""
        return self.reply_driver(self.sp.sendernick, message, c)

    class Channel:

        def __init__(self, fp, name=""):
            self.fp = fp
            self.name = ""
            self.findname(name)

        def findname(self, name=""):
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