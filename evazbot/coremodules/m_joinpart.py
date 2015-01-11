# -*- coding: utf-8 -*-

from base import *


def afterall(mp):
    if mp.isserver():
        return
    if mp.isjp('JOIN') or mp.code('JOIN'):
        main.ircprofiles[main.currentprofile]["adminlist"][mp.ircuser()] = ''
        main.nlistadd(mp.ircuser(), main.getchannel())
        main.whois(mp.ircuser())
    elif mp.isjp('PART') or mp.code('PART'):
        main.ircprofiles[main.currentprofile]["adminlist"][mp.ircuser()] = ''
        main.nlistcheck(mp.ircuser())
        main.ircprofiles[main.currentprofile][
                "nicklist"][
                    mp.ircuser()] = list(filter((main.getchannel()).__ne__,
                main.ircprofiles[main.currentprofile][
                "nicklist"][mp.ircuser()]))
        main.whois(mp.ircuser())
    elif mp.isquit() or mp.code('QUIT'):
        main.ircprofiles[main.currentprofile][
                "nicklist"][mp.ircuser()] = []
        main.ircprofiles[main.currentprofile]["adminlist"][mp.ircuser()] = ''
