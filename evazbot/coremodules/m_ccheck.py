# -*- coding: utf-8 -*-
from base import *

notfoundmessage = '?'

##mconfig/ccheck.py
##options:
#notfoundmessage = 'Command not found.'
exec(c_locs.mconfig("ccheck"))


def afterall(mp):
    if not main.handled and not main.wasserver:
        found = -1
        s1 = 'PRIVMSG ' + main.getchannel() + ' :' + cmd.cprefix
        found = mp.text().find(s1)
        if found == -1:
            s2 = mp.user() + '> ' + cmd.cprefix
            found = mp.text().find(s2)
            if found != -1:
                found += len(s2)
        else:
            found += len(s1)
        if found != -1:
            if mp.text()[found:found + 1].isalnum():
                main.sendcmsg(notfoundmessage)
                for i in c_modules.helpmodulenames():
                    if mp.text().find(cmd.cprefix + i) != -1:
                        main.sendcmsg('If you meant to call module ' + i
                                      + ', use: ' + cmd.cprefix + 'help ' + i)
