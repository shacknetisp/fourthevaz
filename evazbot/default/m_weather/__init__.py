from base import *
from json import loads
from urllib.request import urlopen
from decimal import *
import pygeoip
weather = mload('m_weather.weather')
gi = pygeoip.GeoIP('deps/pygeoip/GeoLiteCity.dat')


def start():
    return ["weather"]


class weatherinfo:
    data = {}

    def getinfo(self, number):
        data = self.data
        name = data["name"]
        cname = data["sys"]["country"]
        if len(name) == 0:
            name = self.dname
        #checks what the request wants
        if number == "currenttemp":
            if self.outputtemp == "kel":
                return "It is " +\
                str(data["main"]["temp"]) +\
                " Kelvin in " + name + ", " + cname
            elif self.outputtemp == "cel":
                temp = Decimal(str(data["main"]["temp"])) - Decimal('273.15')
                return "It is " + str(temp) +\
                " Celcius in " + name + ", " + cname
            elif self.outputtemp == "far":
                temp = Decimal(str(data["main"]["temp"])) - Decimal('273.15')
                temp = Decimal(str(temp)) * Decimal('1.8') + Decimal('32.0')
                return "It is " + str(temp) +\
                " Farenheit in " + name + ", " + cname
            else:
                raise ValueError(
                    "Invalid Temperature Style: " + self.outputtemp)
        elif number == "currentwindspeed":
            return "The Wind is Blowing at " +\
            str(data["wind"]["speed"]) + " m/s in " + name + ", " + cname

    def __init__(self, url, style, altname):
        jsonobj = urlopen(url)
        jsonobj = jsonobj.read()
        self.data = loads(jsonobj.decode())
        self.outputtemp = style
        self.dname = altname


def get(ct):
    if ct.cmd('weather'):
        if ct.args.getbool('wind'):
            info = "windspe"
        elif ct.args.getbool('temp'):
            info = 'temp'
        style = "cel"
        if ct.args.getbool('kel'):
            style = 'kel'
        elif ct.args.getbool('far'):
            style = 'far'
        argument = ct.args.getdef()
        if ct.args.getbool('id'):
            apiform = 'id'
        elif ct.args.getbool('name'):
            apiform = 'name'
        elif ct.args.getbool(geoip):
            apiform = 'geoip'
        ct.msg(weather.printweather(style, info, apiform, argument))


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

