# -*- coding: utf-8 -*-
from configs.module import Module
from configs import match
import configs.mload
import random
import pytz
import utils
from datetime import datetime, tzinfo, timedelta
ZERO = timedelta(0)


class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


def gettimezones(search, maxi):
    timezones = pytz.all_timezones
    random.shuffle(timezones)
    results = []
    for i in timezones:
        if match.matchnocase(i, search, False):
            if len(results) < maxi or maxi == 0:
                results.append(i)
    return results


def gettimezone(search):
    for i in pytz.all_timezones:
        if i.lower() == search.lower():
            return i
    return ""


def init():
    m = Module(__name__)
    m.set_help('Get time in various timezones.')
    m.add_command_hook('findzone',
        {
            'function': findzone,
            'help': 'Get a list of timezones.',
            'args': [
                {
                    'name': 'search',
                    'optional': True,
                    'help': 'Search filter.',
                    },
                ],
            })
    m.add_command_hook('gettime',
        {
            'function': gettime,
            'help': 'Get time.',
            'args': [
                {
                    'name': 'zone/ip',
                    'optional': False,
                    'help': 'Timezone/Hostname/IP to use.',
                    },
                        {
                    'name': 'utc',
                    'optional': True,
                    'help': 'Time UTC to use.',
                    },
                ],
            })
    m.add_command_alias('time', 'gettime')
    return m


def findzone(fp, args):
    r = utils.ltos(gettimezones(args.getlinstr('search', ''), 12))
    return r if r else "No results."


def gettime(fp, args):
    geoip = fp.server.import_module('geoip', False)
    tz = args.getlinstr('zone/ip')
    t = datetime.now(UTC())
    utcs = '%d:%d' % (t.hour, t.minute)
    utc = args.getlinstr('utc', utcs)
    try:
        pytz.timezone(gettimezone(tz))
    except pytz.exceptions.UnknownTimeZoneError:
        r = geoip.geoip(tz)
        try:
            tz = r['timezone']
        except TypeError:
            pass
        except KeyError:
            pass
    try:
        target = pytz.timezone(gettimezone(tz))
    except pytz.exceptions.UnknownTimeZoneError:
        try:
            return('Cannot find timezone, do you mean %s?' % (str(
                random.choice(gettimezones(tz, 0)))))
        except IndexError:
            return('Cannot find timezone, try: findzone <search>')
    try:
        t = t.replace(
            hour=int(utc.split(':')[0]), minute=int(utc.split(':')[1]))
        utcs = '%02d:%02d' % (t.hour, t.minute)
        utcs = 'UTC: ' + utcs
    except IndexError:
        return('Invalid utc format.')
    except ValueError as e:
        return str(e)
    t = t.astimezone(target)
    utcs += ' is %s: %02d:%02d' % (
        tz, t.hour, t.minute)
    return utcs
