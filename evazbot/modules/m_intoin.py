# -*- coding: utf-8 -*-
from base import *


def msg(mp):
    if mp.isserver():
        if mp.text().count(main.getchannel() + " :") == 1:
            if mp.text().find("has left the game") != -1:
                if mp.text().find("kicked") != -1:
                    main.sendcmsg("Kicked out!")
                if mp.text().find("banned") != -1:
                    main.sendcmsg(
                        "Ban? That insolent troublemaker deserved it.")
                if mp.text().find("packet overflow") != -1:
                    main.sendcmsg("The lag is here.")