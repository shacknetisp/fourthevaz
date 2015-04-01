# -*- coding: utf-8 -*-
import configs.module
import configs.mload
import requests


def init():
    m = configs.module.Module(__name__)
    m.set_help('Get weather from http://openweathermap.org.')
    m.add_command_hook('weather', {
        'function': weather,
        'help': 'Get weather results.',
        'args': [
            {
                'name': 'imp',
                'keyvalue': '',
                'help': 'Use the imperial system.',
                'optional': True,
                },
            {
                'name': 'location/IP',
                'optional': False,
                'help': 'Place to view.',
                'end': True,
                },
            ]
        })
    return m


def weather(fp, args):
    geoip = configs.mload.import_module_py(
        'geoip', fp.server.entry['moduleset'], False)
    imperial = ('imp' in args.lin)
    location = args.getlinstr('location/IP')
    r = geoip.geoip(location)
    try:
        location = r['city'] + ',' + r['countryCode']
    except TypeError:
        pass
    except KeyError:
        pass
    p = {
        'q': location,
        }
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params=p)
    json = r.json()
    if json['cod'] != 200:
        return json['message']
    else:
        tempn = json['main']['temp'] - 273.15
        if imperial:
            tempn = (tempn * (9 / 5)) + 32
        temp = '%d°%s' % (tempn, 'F' if imperial else 'C')
        windn = json['wind']['speed']
        if imperial:
            windn = windn * 2.23694
        try:
            gustn = json['wind']['gust']
            if imperial:
                gustn = gustn * 2.23694
            gust = "%d %s gusts" % (gustn,
                'mph' if imperial else 'm/s')
        except KeyError:
            gust = 'no gusts'
        wind = '%d %s, %s, %d°' % (
            windn,
            'mph' if imperial else 'm/s',
            gust,
            json['wind']['deg']
            )
        return "%s, %s: %s; %s; %s" % (
            json['name'],
            json['sys']['country'],
            temp,
            wind,
            json['weather'][0]['description']
            )