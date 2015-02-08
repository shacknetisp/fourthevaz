# -*- coding: utf-8 -*-
from base import *
import pytz
from datetime import datetime, tzinfo, timedelta
import random
c_geoip = cload('c_geoip')

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
    results = []
    for i in pytz.all_timezones:
        if i.lower().find(search.lower()) != -1 or\
        c_regex.casecontains(search, i):
            if len(results) < maxi or maxi == 0:
                results.append(i)
    return results


def gettimezone(search):
    for i in pytz.all_timezones:
        if i.lower() == search.lower():
            return i
    return ""


def start():
    return ["time"]


def get(ct):
    if ct.cmd('time'):
        if ct.args.getbool('findzone'):
            results = ['Results']
            results += gettimezones(ct.args.getdef(), 13)
            cmd.outlist(results)
            return True
        else:
            argument = ct.args.getdef().upper()
            try:
                pytz.timezone(gettimezone(argument))
            except pytz.exceptions.UnknownTimeZoneError:
                ip = ct.args.getdef()
                r = c_geoip.getinfo(ip)
                try:
                    argument = r['time_zone']
                except TypeError:
                    pass
            try:
                target = pytz.timezone(gettimezone(argument))
            except pytz.exceptions.UnknownTimeZoneError:
                try:
                    ct.msg('Cannot find timezone, do you mean %s?' % (str(
                        random.choice(gettimezones(ct.args.getdef(), 0)))))
                except IndexError:
                    ct.msg('Cannot find timezone, try ' +
                    cmd.cprefix() + 'time -getzone <search>')
                return True
            t = datetime.now(UTC())
            utcs = '%d:%d' % (t.hour, t.minute)
            try:
                t = t.replace(hour=int(ct.args.get(
                    'utc', utcs).split(':')[0]), minute=int(ct.args.get(
                        'utc', utcs).split(':')[1]))
                utcs = '%02d:%02d' % (t.hour, t.minute)
                utcs = 'UTC: ' + utcs
            except IndexError:
                main.sendcmsg('Invalid -utc format.')
                return
            except ValueError:
                main.sendcmsg('Invalid -utc format.')
                return
            t = t.astimezone(target)
            utcs += ' is %s: %02d:%02d' % (
                argument, t.hour, t.minute)
            ct.msg(utcs)
            return True
    return False


def showhelp(h):
    h("time [-utc=<00:00>] <timezone/region/ip/host>: " +
    "get current time, or UTC time from -utc")
    h("time -findzone <zonesearch>: " +
    "Get first 12 timezones matching <zonesearch>.")