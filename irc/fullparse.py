# -*- coding: utf-8 -*-


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

    def isquery(self):
        return self.sp.target == self.server.nick

    def outtarget(self):
        if self.isquery():
            return self.sp.sendernick
        else:
            return self.sp.target

    def reply(self, message, command='NOTICE'):
        self.server.write_cmd(command, self.outtarget() + str(' %s' % (
            ':' if command.upper() == 'NOTICE' else '')) + message)

    class Channel:

        def __init__(self, fp):
            self.fp = fp
            self.findname()

        def findname(self):
            for c in self.fp.server.channels:
                if self.fp.sp.target == c['channel']:
                    self.entry = c
                    return
            self.entry = None