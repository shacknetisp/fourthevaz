# -*- coding: utf-8 -*-
from base import *
import pygeoip
gi = pygeoip.GeoIP('deps/pygeoip/GeoLiteCity.dat')


def start():
    return ["weather"]




def printweather(style, info, apiform, argument):
    if info == 'weather':
        tempstyle = None
        returnwind = False
        returntemp = False
        urlid = False
        urlcity = False
        usegeoip = False
        if style == 'cel':
            tempstyle = "cel"
        elif style == 'kel':
            tempstyle = "kel"
        elif style == 'far':
            tempstyle = "far"
        if info == "windspe":
            returnwind = True
        elif info == "temp":
            returntemp = True
        if apiform == "id":
            urlid = True
        elif apiform == "name":
            urlcity = True
        elif apiform == "geoip":
            usegeoip = True
        if usegeoip:
            ip = argument
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
        if not urlid:
            urlcity = True

        if not returntemp and not returnwind:
            main.sendcmsg("Specify what information you want.")
        if (urlcity and urlid):
            main.sendcmsg("You can't have both -name and -id!")
        else:
            jsonurl = 'http://api.openweathermap.org/data/2.5/weather?q=' + \
            argument
            if urlid:
                jsonurl = \
                'http://api.openweathermap.org/data/2.5/weather?id=' + \
                argument
            wxinfo = weatherinfo(jsonurl, tempstyle, argument)
            data = wxinfo.data
            if data["cod"] == 200:
                if returnwind:
                    return(wxinfo.getinfo("currentwindspeed"))
                if returntemp:
                    return(wxinfo.getinfo("currenttemp"))
            elif data["cod"] == "404":
                return(data["cod"] + ":" + data["message"])

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
        cmd.cprefix() + "weather [-temp] [-wind] [-cel -kel -far] [-name -id]" +
        "<city name/id>:" +
        " Get weather from http://openweathermap.org")
    main.sendcmsg("-temp, -wind: Get temperature, wind.")
    main.sendcmsg(
        "-cel, -kel, -far: Use celsius, kelvin, farenheit, -cel is default.")
    main.sendcmsg(
        "-name, -id, -geoip: Use city name or ID or GeoIP, -name is default.")
