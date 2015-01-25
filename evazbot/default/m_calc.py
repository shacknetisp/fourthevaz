from base import *


def start():
    return ["calc"]


def msg(mp):
    if mp.cmd('calc'):
        arg = mp.argsdef()
        try:
            main.sendcmsg('(%s) = (%s)' % (
                arg, str(c_safeeval.domath(arg))))
        except Exception as e:
            main.sendcmsg('Error: ' + str(e))
        return True
    return False


def showhelp(h):
    h('calc <mathematical expression>: Calculate a math expression.')