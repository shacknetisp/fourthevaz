# -*- coding: utf-8 -*-
from base import *
c_geoip = cload('c_geoip')
import re
enable_geoip = False
##mconfig/geoip.py
##options:
#enable_geoip = True #Give country when someone connects to a server
exec(c_locs.mconfig("geoip"))


def start():
    print(('GeoIP Server Login: ' + str(enable_geoip)))
    return ["geoip"]


def msg(mp):
    if mp.isserver() and mp.text().find(') has joined the game') != -1 \
        and enable_geoip:
        ip = re.findall(' \((.*?)\) has', mp.text())[-1]
        r = c_geoip.getinfo(ip)
        try:
            index = mp.text().index(' (' + ip)
        except ValueError:
            index = len(s)
        try:
            main.sendcmsg(mp.text()[mp.text().index(' :') + 2:index]
                          + ': ' + r['country_name'])
            return True
        except TypeError:
            pass
        try:
            index = mp.text().index(' (' + ip)
        except ValueError:
            index = len(s)
        main.sendcmsg(mp.text()[mp.text().index(' :') + 2:index] + ': '
                      + 'Unknown')
        return True
    if mp.wcmd('geoip'):
        ip = mp.argsdef()
        r = c_geoip.getinfo(ip)
        try:
            main.sendcmsg(r['city'] + ', ' + r['region'] + ', '
                          + r['country'])
        except TypeError:
            main.sendcmsg('Cannot get information.')
        return True
    return False


def showhelp():
    main.sendcmsg(cmd.cprefix() +
    'geoip <ip>: Find location information from IP address.'
                  )
