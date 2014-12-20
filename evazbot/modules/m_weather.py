# -*- coding: utf-8 -*-
from base import *
from json import loads
from urllib.request import urlopen
from decimal import *


class weatherinfo:
    data = {}
    outputtemp = "kel"

    def getinfo(self, number):
        data = self.data
        #checks what the request wants
        if number == "currenttemp":
            if self.outputtemp == "kel":
                return "It is " +\
                str(data["main"]["temp"]) + " in " + data["name"]
            elif self.outputtemp == "cel":
                temp = Decimal(str(data["main"]["temp"])) - Decimal('273.15')
                return "It is " + str(temp) + " in " + data["name"]
            elif self.outputtemp == "far":
                temp = Decimal(str(data["main"]["temp"])) - Decimal('273.15')
                temp = Decimal(str(temp)) * Decimal('1.8') + Decimal('32.0')
                return "It is " + str(temp) + " in " + data["name"]
        elif number == "currentwindspeed":
            return "The Wind is Blowing at " +\
            str(data["wind"]["speed"]) + " m/s"

    def __init__(self, url, style="kel"):
        jsonobj = urlopen(url)
        jsonobj = jsonobj.read()
        self.data = loads(jsonobj.decode())
        self.outputtemp = style


def msg(mp):
    if mp.cmd('weather'):
        tempstyle = "kel"
        if mp.argbool('cel'):
            tempstyle = "cel"
        elif mp.argbool('kel'):
            tempstyle = "kel"
        elif mp.argbool('far'):
            tempstyle = "far"
        returnwind = mp.argbool('wind')
        urlid = mp.argbool('id')
        urlcity = mp.argbool('name')
        returntemp = mp.argbool('temp')
        #funtion that gets the info to be displayed

        if not returntemp and not returnwind:
            main.sendcmsg("Specify what information you want.")

        if (urlcity and urlid) or (returnwind and returntemp):
            main.sendcmsg("You can't have both!")
        elif urlcity:
            jsonurl = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
            mp.argsdef()
            wxinfo = weatherinfo(jsonurl, tempstyle)
            data = wxinfo.data
            if data["cod"] == 200:
                if returnwind:
                    main.sendcmsg(wxinfo.getinfo("currentwindspeed"))
                elif returntemp:
                    main.sendcmsg(wxinfo.getinfo("currenttemp"))
            elif data["cod"] == "404":
                main.sendcmsg(data["cod"] + ":" + data["message"])
        elif urllid:
            jsonurl = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
            mp.argsdef()
            wxinfo = weatherinfo(jsonurl)
            data = wxinfo.data
            if data["cod"] == 200:
                if returnwind:
                    main.sendcmsg(wxinfo.getinfo("currentwindspeed"))
                elif returntemp:
                    main.sendcmsg(wxinfo.getinfo("currenttemp"))
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
    main.sendcmsg("        -name: Looks up info by city name. " +
    "Please use the closest large town")
    main.sendcmsg("        -id: Looks up by city id")
    main.sendcmsg("        -wind: Finds wind information")