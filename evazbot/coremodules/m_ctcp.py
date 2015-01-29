# -*- coding: utf-8 -*-
from base import *
import platform
import OS


def get(ct):
    def replyctcp(message):
        ct.msg("\x01" + message + "\x01", '', "NOTICE")

    def isctcp(command):
        return ct.text().find("\x01" + command) != -1

    if isctcp("VERSION"):
        t = platform.python_version_tuple()
        replyctcp("VERSION " +
        ct.botname() + " runs on Python " +
        str(t[0]) + "." + str(t[1]) + "." + str(t[2]))
        replyctcp('Running on ' + platform.platform())
        return True
    elif isctcp("PING"):
        replyctcp("PING " + ct.getsplit(4).strip('\x01'))
        return True
    return False
