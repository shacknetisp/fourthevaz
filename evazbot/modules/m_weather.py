# -*- coding: utf-8 -*-
from base import *
from json import loads
from urllib.request import urlopen
from decimal import *
import pygeoip
gi = pygeoip.GeoIP('pygeoip/GeoLiteCity.dat')

class weatherinfo:
    data = {}

    def getinfo(self, number):
        data = self.data
        #checks what the request wants
        if number == "currenttemp":
            if self.outputtemp == "kel":
                return "It is " +\
                str(data["main"]["temp"]) + " kel in " + data["name"]
            elif self.outputtemp == "cel":
                temp = Decimal(str(data["main"]["temp"])) - Decimal('273.15')
                return "It is " + str(temp) + " cel in " + data["name"]
            elif self.outputtemp == "far":
                temp = Decimal(str(data["main"]["temp"])) - Decimal('273.15')
                temp = Decimal(str(temp)) * Decimal('1.8') + Decimal('32.0')
                return "It is " + str(temp) + " far in " + data["name"]
            else:
                raise ValueError(
                    "Invalid Temperature Style: " + self.outputtemp)
        elif number == "currentwindspeed":
            return "The Wind is Blowing at " +\
            str(data["wind"]["speed"]) + " m/s in " + data["name"]

    def __init__(self, url, style):
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
        usegeoip = mp.argbool('geoip')
        argument = mp.argsdef()
        if usegeoip:
            ip = mp.argsdef()
            urlid = False
            urlcity = True
            try:
                r = gi.record_by_addr(ip)
            except:
                try:
                    r = gi.record_by_name(ip)
                except:
                    r = None
            try:
                argument = r['city'] + ', ' + r['region_code'] + ', '\
                        + r['country_code']
                main.sendcmsg("Using: " + argument)
            except TypeError:
                main.sendcmsg('Cannot get GeoIP information.')
                return True
        if not urlid:
            urlcity = True
        returntemp = mp.argbool('temp')
        #funtion that gets the info to be displayed

        if not returntemp and not returnwind:
            main.sendcmsg("Specify what information you want.")
            return True
        if (urlcity and urlid):
            main.sendcmsg("You can't have both -name and -id!")
        else:
            jsonurl = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
            argument
            if urlid:
                jsonurl = \
                'http://api.openweathermap.org/data/2.5/weather?id=' + \
                argument
            wxinfo = weatherinfo(jsonurl, tempstyle)
            data = wxinfo.data
            if data["cod"] == 200:
                if returnwind:
                    main.sendcmsg(wxinfo.getinfo("currentwindspeed"))
                if returntemp:
                    main.sendcmsg(wxinfo.getinfo("currenttemp"))
            elif data["cod"] == "404":
                main.sendcmsg(data["cod"] + ":" + data["message"])

'''
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
'''


def showhelp():
    main.sendcmsg(
        ".weather [-temp] [-wind] [-cel -kel -far] [-name -id]" +
        "<city name/id>:" +
        " Get weather from http://openweathermap.org")
    main.sendcmsg("-temp, -wind: Get temperature, wind.")
    main.sendcmsg("-cel, -kel, -far: Use celsius, kelvin, farenheit.")
    main.sendcmsg(
        "-name, -id, -geoip: Use city name or ID or GeoIP, -name is default.")