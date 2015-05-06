# -*- coding: utf-8 -*-
import base.fullparse


class FullParse(base.fullparse.FullParse):

    def __init__(self, server, text):
        super(FullParse, self).__init__(server, nomore=True)
        self.text = text
        """SplitParser object."""
        self.user = "file"
        """
        User name.
        """
        self.setaccess("%s=%s=%s" % (
            self.user, "", ""))

    def room(self):
        """Return the current 'room'."""
        return "file"

    def reply_driver(self, message):
        for m in message.split('\n'):
            self.server.output(m)

    def hasright(self, right):
        """Returns if the user has the specified right."""
        access = self.server.import_module('rights.access', False)
        extra = []
        return (right in (access.fullrights(self, access.getrights(
            self.server, self.accesslevelname) + extra)))

    def reply(self, message):
        """Default reply function, reply with <message> [command <c>]."""
        return self.reply_driver(message)

    def replypriv(self, message):
        """Reply privately."""
        return self.reply_driver(message)

    def canuse(self, module, command=''):
        """Return if the user can use <module>[.<command>]"""
        for r in [':' + module,
            ':' + module + '.' + command]:
                dr = '-' + r
                if self.hasright(dr):
                    return False
        return True