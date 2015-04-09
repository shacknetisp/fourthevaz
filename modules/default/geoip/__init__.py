# -*- coding: utf-8 -*-
import requests
import configs.module


def init():
    m = configs.module.Module('geoip')
    m.set_help('Get IP information.')
    m.add_command_hook('geoip',
        {
            'function': dogeoip,
            'help': 'Get IP Information.',
            'args': [
                {
                    'name': 'ip',
                    'optional': False,
                    'help': 'The IP or Hostname to look up.'
                    },
                {
                    'name': 'lookup',
                    'optional': True,
                    'help': 'A list of information to view, from: '
                    'country, countryCode, region, regionName, city, zip, '
                    'lat, lon, timezone, isp, org, as, reverse, query',
                    },
                ],
            }
        )
    m.add_alias('geoipnick', 'geoip <whois $# host> $*')
    return m


def dogeoip(fp, args):
    ip = args.getlinstr('ip')
    lookup = args.getlinstr('lookup', 'query,city,region,country').split(',')
    result = geoip(ip, True if 'reverse' in lookup else False)
    if result['status'] == 'fail':
        return "Error: %s" % result['message']
    output = ""
    for l in lookup:
        try:
            output += "%s: %s; " % (l, result[l])
        except KeyError:
            return "%s is not in the results." % (l)
    return(output.strip())


def geoip(inp, useall=False):
    response = requests.get(
            str('http://ip-api.com/json/%s%s' % (
                inp, '?fields=65535' if useall else ''))
        )
    ret = response.json()
    return ret