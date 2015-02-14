# -*- coding: utf-8 -*-
from base import *
import platform
import datetime
import time

userinfo = "<no user info set>"

##mconfig/ctcp.py
##lines of the following:
#userinfo = "user info goes here"
exec(c_locs.mconfig("ctcp"))


def get(ct):
    def replyctcp(command, message):
        ct.msg("\x01" + command + ' ' + message + "\x01", '', "NOTICE")

    def isctcp(command):
        return ct.text().find("\x01" + command) != -1

    if isctcp("VERSION"):
        t = platform.python_version_tuple()
        replyctcp("VERSION", str(
            "{name} | Python {t[0]}.{t[1]}.{t[2]} |"
            + " OS: {pv}").format(**
            {
                't': t,
                'pv': platform.platform(),
                'name': ct.botname(),
                }))
        return True
    elif isctcp("PING"):
        replyctcp("PING", ct.getsplit(4).strip('\x01'))
        return True
    elif isctcp('SOURCE'):
        replyctcp('SOURCE', 'http://github.com/shacknetisp/fourthevaz')
        return True
    elif isctcp('TIME'):
        val = (time.timezone / 60 / 60)
        replyctcp('TIME', str(datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S GMT ') + str("" if val < 0 else "+") + str(
                val)))
        return True
    elif isctcp('USERINFO'):
        replyctcp('USERINFO', userinfo)
        return True
    elif isctcp('FINGER'):
        replyctcp('FINGER', ct.botname())
        return True
    elif isctcp('ERRMSG'):
        replyctcp('ERRMSG', "Invalid Data")
        return True
    elif isctcp('CLIENTINFO'):
        replyctcp('CLIENTINFO',
            'VERSION PING SOURCE TIME CLIENTINFO USERINFO FINGER ERRMSG')
        return True
    elif isctcp('DCC CHAT CHAT'):
        main.connectdcc(
            ct.ircuser(), ct.getsplit(6), ct.getsplit(7).strip('\x01'),
            ct.getwlevel(ct.ircuser()))
        return True
    return False
