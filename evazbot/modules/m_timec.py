from base import *
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import traceback
from tzlocal import get_localzone


def tuntil(mp,f):
    tdelta = datetime.utcnow() - datetime.strptime(mp.argsdef().strip(), f+"/%y %H:%M");
    seconds = (tdelta.microseconds + (tdelta.seconds + tdelta.days * 24 * 3600) * 10**6) / 10**6
    main.sendcmsg(str(round(abs(seconds/3600),2))+" hours")

def msg(mp):
    if mp.cmd("time utc"):
        main.sendcmsg(datetime.utcnow().strftime("%H:%M"))
        return True
    if mp.cmd("time until"):
        try:
            if mp.argbool("dmy"):
                tuntil(mp,"%d/%m")
            else:
                tuntil(mp,"%m/%d")
        except ValueError:
            main.sendcmsg("Bad time format, possibly a number is wrong. (00:00, not 24:00?)")
        return True
    return False


def showhelp():
    main.sendcmsg(".time utc: Get current UTC time.")
    main.sendcmsg(".time until [-dmy] <d/m/y H:M>: Get hours and minutes until <date> utc. Default is -mdy.")
