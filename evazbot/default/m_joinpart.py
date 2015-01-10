# -*- coding: utf-8 -*-

from base import *

announce_entries = False
##mconfig/joinpart.py
#announce_entries = True #show message for joining, parting, and quitting
exec(c_locs.mconfig('joinpart'))


def msg(mp):
    if mp.isserver():
        return
    if mp.isjp('JOIN'):
        main.ircprofiles[main.currentprofile]["adminlist"][mp.ircuser()] = ''
        main.whois(mp.ircuser())
        if announce_entries:
            main.sendamsg(cmd.getname(mp.ircuser()) + ' is now in '
                     + main.getchannel() + '.')
    elif mp.isjp('PART'):
        main.ircprofiles[main.currentprofile]["adminlist"][mp.ircuser()] = ''
        if announce_entries:
            main.sendamsg(cmd.getname(mp.ircuser()) + ' has departed '
                      + main.getchannel() + '.')
    elif mp.isquit():
        main.ircprofiles[main.currentprofile]["adminlist"][mp.ircuser()] = ''
        if announce_entries:
            main.sendamsg(cmd.getname(mp.ircuser()) + ' has left IRC.')
