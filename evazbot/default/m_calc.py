from base import *
reload(c_safeeval)


def start():
    return ["calc"]


def msg(mp):
    if mp.cmd('calc'):
        arg = mp.argsdef()
        try:
            main.sendcmsg('(%s) = (%s)' % (
                arg, str(float(c_safeeval.domath(arg)))))
        except Exception as e:
            main.sendcmsg('Error: ' + str(e))
        return True
    return False


def showhelp(h):
    h('calc <mathematical expression>: Calculate a math expression.')