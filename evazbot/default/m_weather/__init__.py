from base import *
import pygeoip
import requests
import xmltodict
weather = mload('m_weather.weather')
forecast = mload('m_weather.forecast')
gi = pygeoip.GeoIP('deps/pygeoip/GeoLiteCity.dat')


def start():
    return ["weather"]


def get(ct):
    if ct.cmd('weather'):
        info = []
        weatherstyle = "weather"
        if ct.args.getbool('wind'):
            info.append('windspe')
        if ct.args.getbool('temp'):
            info.append('temp')
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
        lastmsg = ""
        for i in info:
            thismsg = weather.printweather(
                weatherstyle, style, i, apiform, argument, gi)
            if thismsg != lastmsg:
                ct.msg(thismsg)
            lastmsg = thismsg
    elif ct.cmd('forecast'):
        opt = {'mode': 'xml'}
        if (not ct.args.getbool('id')) and (not ct.args.getbool('name')) and (not ct.args.getbool('geoip')):
            ct.msg('Specify an input method!')
        elif ct.args.getbool('name'):
            opt['q'] = ct.args.getdef()
        elif ct.args.getbool('id'):
            opt['id'] = ct.args.getdef()
        elif ct.args.getbool('geoip'):
            ip = ct.args.getdef()
            urlid = False
            #urlcity = True
            try:
                r = gi.record_by_addr(ip)
            except:
                try:
                    r = gi.record_by_name(ip)
                except:
                    r = None
            try:
                opt['q'] = r['city'] + ', ' + r['region_code'] + ', '\
                        + r['country_code']
            except TypeError:
                ct.msg('Cannot get GeoIP information.')
        try:
            opt['cnt'] = ct.args.get('days')
        except ValueError:
            opt['cnt'] = 7

        url = 'http://api.openweathermap.org/data/2.5/forecast/daily'
        r = requests.get(url, params=opt)
        data = xmltodict.parse(r.text)
        data = data['weatherdata']['forecast']['time']
        info = []
        for i in ct.args.getlist():
            if i in data:
                subdict = data[i]
                sub = ct.args.get(i)
                for o in sub.split(','):
                    if o in subdict:
                        info.append([i, '@' + o])
                    else:
                        info.append([i, '@' + list(subdict.keys()[0])])
        forecastdata = forecast.printforecast(info,data)
        forecastdata = forecastdata.split('\n')
        for i in forecastdata:
            ct.msg(i)



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
