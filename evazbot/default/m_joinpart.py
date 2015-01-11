# -*- coding: utf-8 -*-

from base import *


def msg(mp):
    if mp.isserver():
        return
    if mp.isjp('JOIN') or mp.code('JOIN'):
        main.ircprofiles[main.currentprofile]["adminlist"][mp.ircuser()] = ''
        main.whois(mp.ircuser())
    elif mp.isjp('PART') or mp.code('PART'):
        main.ircprofiles[main.currentprofile]["adminlist"][mp.ircuser()] = ''
        main.whois(mp.ircuser())
    elif mp.isquit() or mp.code('QUIT'):
        main.ircprofiles[main.currentprofile]["adminlist"][mp.ircuser()] = ''
