# -*- coding: utf-8 -*-


class SplitParser():
    """Low level parser, provides information from the message."""

    def __init__(self, message):
        self.message = message
        self.splitmessage = message.split(' ')
        self.sender = self.getsplit(0)
        try:
            self.sendernick = self.sender[
                self.sender.index(':') + 1:self.sender.index('!')]
        except ValueError:
            self.sendernick = ""
        self.command = self.getsplit(1).upper()
        self.target = self.getsplit(2)
        self.object = self.getsplit(3)
        try:
            self.host = self.sender[
                self.sender.index('~'):]
        except ValueError:
            self.host = ""
        try:
            self.text = self.message[self.message.index(' :') + 2:]
        except ValueError:
            self.text = ""

    def getsplit(self, n, d=''):
        """Get word <n> from the message, with <d> as the default."""
        try:
            return self.splitmessage[n]
        except IndexError:
            return d

    def iscode(self, c):
        """Detect a command."""
        if c == 'endmotd':
            if self.command == '376':
                return True
        elif c == 'kick':
            if self.command == 'KICK':
                return True
        elif c == 'names':
            if self.command == '353':
                return True
        elif c == 'ping':
            if self.command == 'PING':
                return True
        elif c == 'chat':
            if self.command == 'NOTICE' or self.command == 'PRIVMSG':
                return True
        elif c.upper() == self.command:
            return True
        return False
