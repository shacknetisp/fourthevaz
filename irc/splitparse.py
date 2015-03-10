# -*- coding: utf-8 -*-


class SplitParser():

    def __init__(self, message):
        self.message = message
        self.splitmessage = message.split(' ')
        self.sender = self.getsplit(0)
        self.command = self.getsplit(1).upper()
        self.target = self.getsplit(2)
        self.object = self.getsplit(3)

    def getsplit(self, n, d=''):
        try:
            return self.splitmessage[n]
        except IndexError:
            return d

    def iscode(self, c):
        #End of /MOTD command.
        if c == 'endmotd':
            if self.command == '376':
                return True
        elif c == 'kick':
            if self.command == 'KICK':
                return True
        else:
            raise ValueError('Invalid Value for "c".')
        return False
