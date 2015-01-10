# -*- coding: utf-8 -*-
from base import *
import string
import random
earcharsl = '<([{!/\\\'"'
earcharsr = '>)]}!\\/\'"'
eyechars = '*oO0$^'
mouthchars = '._-~'
maxdots = 32
##mconfig/dot.py
##options:
#earcharsl     += '#'
#earcharsr     += '#'
#eyechars      += 'i'
#mouthchars    += '|'
#maxdots = 64 #uses just a bit more CPU
exec(c_locs.mconfig("dot"))


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def sendout(text):
    main.sendcmsg(text)


def msg(mp):
    possible = ""
    for i in range(maxdots):
        if cmd.getcmd(mp.text(), possible, '.'):
            earchari = random.randrange(int(-(min(len(earcharsl),
                                        len(earcharsr)) * 0.5)),
                                        min(len(earcharsl), len(earcharsr)))
            if earchari >= 0:
                sendout(earcharsl[earchari] + id_generator(1,
                              eyechars) + id_generator(1, mouthchars)
                              + id_generator(1, eyechars)
                              + earcharsr[earchari])
            else:
                sendout(id_generator(1, eyechars) + id_generator(1,
                              mouthchars) + id_generator(1, eyechars))
            return True
        possible += "."
    return False
