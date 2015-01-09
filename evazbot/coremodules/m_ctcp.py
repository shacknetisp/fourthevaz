# -*- coding: utf-8 -*-
from base import *
import platform


def msg(mp):
    if mp.text().find("\x01VERSION") != -1:
        t = platform.python_version_tuple()
        main.sendcmsg("\x01" +
        "VERSION " +
        main.botname() + " runs on Python " +
        str(t[0]) + "." + str(t[1]) + "." + str(t[2]) +
        "\x01",
        "NOTICE")
        return True
    elif mp.text().find("\x01PING") != -1:
        main.sendcmsg("\x01" +
        "PING " + mp.text().split()[4],
        "NOTICE")
        return True
    return False