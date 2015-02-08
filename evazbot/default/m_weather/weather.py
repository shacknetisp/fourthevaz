# -*- coding: utf-8 -*-
from base import *
weatherinfo = mload('m_weather.weatherinfo').weatherinfo
c_geoip = cload('c_geoip')


def printweather(ws, style, info, apiform, argument, gi):
    if ws == 'weather':
        tempstyle = None
        urlid = False
        #urlcity = False
        usegeoip = False
        if style == 'cel':
            tempstyle = "cel"
        elif style == 'kel':
            tempstyle = "kel"
        elif style == 'far':
            tempstyle = "far"
        if apiform == "id":
            urlid = True
        #elif apiform == "name":
            #urlcity = True
        elif apiform == "geoip":
            usegeoip = True
        if usegeoip:
            ip = argument
            urlid = False
            #urlcity = True
            r = c_geoip.getinfo(ip)
            try:
                argument = r['city'] + ', ' + r['region_code'] + ', '\
                        + r['country_code']
            except TypeError:
                return('Cannot get GeoIP information.')
        #if not urlid:
            #urlcity = True

        if not info == "temp" and not info == "windspe":
            return("Specify what information you want.")
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
                return(wxinfo.getcurrentinfo(info))
            elif data["cod"] == "404":
                return(data["cod"] + ":" + data["message"])
