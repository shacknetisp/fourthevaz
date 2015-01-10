from base import *
import urllib.request
import urllib.parse
import subprocess
calccmd = "calc"
##mconfig/calc.py
##options:
#calccmd = "mycalculator" #calculator command, must use stdin and stdout
exec(c_locs.mconfig("calc"))


def msg(mp):
    if mp.cmd('calc'):
        arg = mp.argsdef()
        if arg.find('read') == -1 or arg.find('help') == -1:
            p = subprocess.Popen(calccmd + " -- '" + arg + "'", shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            (out, err) = p.communicate()
            main.sendcmsg(out.decode().strip())
        else:
            main.sendcmsg(
                'Detected potentially harmful argument.' +
                'Use math expressions only!'
                          )
        if (len(out.decode()) == 0 and len(err.decode()) == 0)\
        or err.decode().find(calccmd + ": not found") != -1:
            out = urllib.request.urlopen(
                    "https://www.calcatraz.com/calculator/api?c=" +
                    urllib.parse.quote_plus(arg)).read().decode().strip()
            if out == "answer" or out == "":
                out = "invalid"
            main.sendcmsg(out)
        return True
    return False


def showhelp():
    main.sendcmsg(
        cmd.cprefix() + 'calc <mathematical expression>: Calculate a math expression.'
                  )