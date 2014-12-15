# -*- coding: utf-8 -*-
from base import *
import random

lagtext = [
    "The lag is here.",
    "Retrieve the packets!",
    ]
bantext = [
    "Ban? That insolent troublemaker deserved it.",
    "Justice hath been served!",
    "Observe! The sentence has been carried out.",
    ]
kicktext = [
    "Kicked out!",
    "Suddenly, Adieu!",
]


def msg(mp):
    if mp.isserver():
        if mp.text().count(main.getchannel() + " :") == 1:
            if mp.text().find("has left the game") != -1:
                if mp.text().find("kicked") != -1:
                    main.sendcmsg(random.choice(kicktext))
                if mp.text().find("banned") != -1:
                    main.sendcmsg(
                        random.choice(bantext))
                if mp.text().find("packet overflow") != -1:
                    main.sendcmsg(random.choice(lagtext))