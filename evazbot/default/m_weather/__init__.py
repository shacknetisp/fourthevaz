from base import *
import pygeoip
weather = mload('m_weather.weather')
gi = pygeoip.GeoIP('deps/pygeoip/GeoLiteCity.dat')


def start():
    return ["weather"]


def get(ct):
    if ct.cmd('weather'):
        weatherstyle = "weather"
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
        apiform = 'name'
        if ct.args.getbool('id'):
            apiform = 'id'
        elif ct.args.getbool('name'):
            apiform = 'name'
        elif ct.args.getbool("geoip"):
            apiform = 'geoip'
        ct.msg((weather.printweather(
            weatherstyle, style, info, apiform, argument, gi)))


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

