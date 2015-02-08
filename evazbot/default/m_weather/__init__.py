from base import *
c_geoip = cload('c_geoip')
import requests
import xmltodict
weather = mload('m_weather.weather')
forecast = mload('m_weather.forecast')

counter = 0
queue = []
caller = ''


def start():
    return ["weather"]


def tick():
    global counter
    global queue
    global caller
    if not queue == []:
        main.sendmsg(caller, queue[0])
        queue.pop(0)
        counter -= 1


def get(ct):
    global caller
    global counter
    global queue
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
                weatherstyle, style, i, apiform, argument)
            if thismsg != lastmsg:
                ct.msg(thismsg)
            lastmsg = thismsg
    elif ct.cmd('forecast'):
        caller = ct.ircuser()
        opt = {'mode': 'xml'}
        if ct.args.getbool('absdate'):
            date = True
        else:
            date = False
        if ((not ct.args.getbool('id')) and
        (not ct.args.getbool('name')) and (not ct.args.getbool('geoip'))):
            ct.msg('Specify an input method!')
        elif ct.args.getbool('name'):
            opt['q'] = ct.args.getdef()
        elif ct.args.getbool('id'):
            opt['id'] = ct.args.getdef()
        elif ct.args.getbool('geoip'):
            ip = ct.args.getdef()
            #urlid = False
            #urlcity = True
            r = c_geoip.getinfo(ip)
            try:
                opt['q'] = r['city'] + ', ' + r['countryCode']
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
            for obj in data[0]:
                if i == obj:
                    subdict = data[0][i]
                    sub = ct.args.get(i)
                    for o in sub.split(','):
                        for a in subdict:
                            if '@' + o == a:
                                info.append([i, '@' + o])
        forecastdata = forecast.printforecast(info, data, date)
        forecastdata = forecastdata.split('\n')
        for i in forecastdata:
            if counter < 11:
                ct.msg(i, ct.ircuser())
                counter += 1
            else:
                queue.append(i)


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
