# -*- coding: utf-8 -*-
from base import *


def afterall(mp):
    if not main.handled and not main.wasserver:
        if mp.text().find('PRIVMSG ' +
        main.getchannel() + ' :' + cmd.cprefix) != -1 \
            or mp.text().find(mp.user() + '> ' + cmd.cprefix) != -1:
            main.sendcmsg('Unrecognized Command!')
            for i in c_modules.helpmodulenames():
                if mp.text().find(cmd.cprefix + i) != -1:
                    main.sendcmsg('If you meant to call module ' + i
                                  + ', use: ' + cmd.cprefix + '.help ' + i)
