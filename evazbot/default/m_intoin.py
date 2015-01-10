# -*- coding: utf-8 -*-
from base import *
import random

lagtext = [
    "The lag is here.",
    "Retrieve the packets!",
    "Bow to the lag, it has conquered yet again.",
    ]
bantext = [
    "Ban? That insolent troublemaker deserved it.",
    "Justice hath been served!",
    "The hammer of justice has fallen.",
    ]
kicktext = [
    "Kicked out!",
    "Suddenly, Adieu!",
    "Try again!",
]

##mconfig/intoin.py
##options:
#lagtext.append('lag out message')
#bantext.append('ban message')
#kicktext.append('kick message')
exec(c_locs.mconfig("intoin"))


def msg(mp):
    if mp.isserver() or mp.cmd("intoin"):
        if mp.text().count(main.getchannel() + " :") == 1:
            if mp.text().find("has left the game") != -1:
                if mp.text().find("kicked") != -1:
                    main.sendcmsg(random.choice(kicktext))
                if mp.text().find("banned") != -1:
                    main.sendcmsg(
                        random.choice(bantext))
                if mp.text().find("packet overflow") != -1:
                    main.sendcmsg(random.choice(lagtext))