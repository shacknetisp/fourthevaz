import base
base.reload(base)
from base import *


def start():
    return ["calc"]


def msg(mp):
    if mp.cmd('calc'):
        arg = mp.argsdef()
        main.sendcmsg('(%s) = (%s)' % (
            arg, str(c_safeeval.domath(arg))))
        return True
    return False


def showhelp(h):
    h('calc <mathematical expression>: Calculate a math expression.')