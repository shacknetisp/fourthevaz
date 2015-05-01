# -*- coding: utf-8 -*-


class FullParse():
    """
    High-level parser, contains Server and SplitParse references.
    """

    def __init__(self, server, nomore=False):
        self.server = server
        """Current Server"""
        self.nomore = nomore
        self.isexternal = False
        self.moreflag = False
        self.type = server.type

    def execute(self, command):
        """Execute <command> with the commands module."""
        commands = self.server.import_module('commands', False)
        return commands.doptext(self, command)

    def external(self):
        """Returns true if the messages comes from a server relay."""
        return self.isexternal

    def setaccess(self, s=""):
        """Set the access string of this fullparse object."""
        if s:
            self.accesslevelname = s