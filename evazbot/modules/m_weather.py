# -*- coding: utf-8 -*-
from base import *
from json import loads
from urllib.request import urlopen

def msg(mp):
    if mp.cmd('weather'):
        outputcel = mp.argbool('cel')
        outputfar = mp.argbool('far')
        outputkel = mp.argbool('kel')
        outputtemp = mp.argbool('temp')
        urlid = mp.argbool('id')
        urlcity = mp.argbool('name')
        if urlcity and urlid:
            main.sendcmsg("You can't have both!")
        elif urlcity and not urlid:
            jsonurl = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
            mp.argsdef()
            jsonobj = urlopen(jsonurl)
            jsonobj = jsonobj.read()
            data = loads(jsonobj)
            if data["cod"] == 200:
                if outputcel:
                    main.sendcmsg(str(data["main"]["temp"] - 273.15))
