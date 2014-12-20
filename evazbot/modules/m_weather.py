# -*- coding: utf-8 -*-
from base import *
from json import loads
from urllib.request import urlopen
from decimal import *



def msg(mp):

    if mp.cmd('weather'):
        outputcel = mp.argbool('cel')
        outputfar = mp.argbool('far')
        outputkel = mp.argbool('kel')
        returnwind = mp.argbool('wind')
        urlid = mp.argbool('id')
        urlcity = mp.argbool('name')
        returntemp = mp.argbool('temp')
        #funtion that gets the info to be displayed

        def getinfo(url, number):
            jsonobj = urlopen(jsonurl)
            jsonobj = jsonobj.read()
            data = loads(jsonobj.decode())
        #checks what the request wants
            if number == "currenttemp":
                if outputkel:
                    return "It is " + str(data["main"]["temp"]) + " in" + data["name"]
                elif outputcel:
                    temp = Decimal(str(data["main"]["temp"])) - Decimal('273.15')
                    return "It is " + str(temp) + " in" + data["name"]
                elif outputfar:
                    temp = Decimal(str(data["main"]["temp"])) - Decimal('273.15')
                    temp = Decimal(str(temp)) * Decimal('1.8') + Decimal('32.0')
                    return "It is " + str(temp) + " in" + data["name"]
            elif number == "currentwindspeed":
                return "The Wind is Blowing at " + str(data["wind"]["speed"]) + " m/s"
        if (urlcity and urlid) or (returnwind and returntemp):
            main.sendcmsg("You can't have both!")
        elif urlcity:
            jsonurl = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
            mp.argsdef()
            if data["cod"] == 200:
                if returnwind:
                    main.sendcmsg(getinfo(jsonurl, "currentwind"))
                elif returntemp:
                    main.sendcmsg(getinfo(jsonurl, "currenttemp"))
            elif data["cod"] == "404":
                main.sendcmsg(data["cod"] + ":" + data["message"])
        elif urllid:
            jsonurl = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
            mp.argsdef()
            if data["cod"] == 200:
                if returnwind:
                    main.sendcmsg(getinfo(jsonurl, "currentwind"))
                elif returntemp:
                    main.sendcmsg(getinfo(jsonurl, "currenttemp"))
            elif data["cod"] == "404":
                main.sendcmsg(data["cod"] + ":" + data["message"])

def showhelp():
    main.sendcmsg(
        'Weather is a module that returns many usefull weather information.'
        )
    main.sendcmsg('This module uses OpenWeatherMap api (openweathermap.org)')
    main.sendcmsg("")
    main.sendcmsg('There are several options listed below:')
    main.sendcmsg('        -cel: Returns answer in celcius')
    main.sendcmsg("        -far: Returns answer in Farenheit")
    main.sendcmsg("        -kel: Returns answer in Kelvin")
    main.sendcmsg("        -name: Looks up info by city name. Please use the closest large town")
    main.sendcmsg("        -id: Looks up by city id")
    main.sendcmsg("        -wind: Finds wind information")