# -*- coding: utf-8 -*-
import configs.module
import configs.match
from . import redflare
import importlib
importlib.reload(redflare)
import utils


def init(options):
    if 'redflares' not in options['server'].db:
        options['server'].db['redflares'] = {}
    m = configs.module.Module(__name__)
    m.set_help('Operate on RedFlares.')
    m.add_command_hook('redflare', {
        'function': doredflare,
        'help': 'Search players on a RedFlare.',
        'args': [
            {
                'name': 'url',
                'optional': False,
                'help': 'URL of the redflare\'s report page.',
                },
            {
                'name': 'stats',
                'keyvalue': '',
                'optional': True,
                'help': 'Show statistics.',
                },
            {
                'name': 'search',
                'optional': True,
                'end': True,
                'help': 'Player to search for.',
                },
            ]
        })
    m.add_command_hook('enableredflare', {
        'function': enableredflare,
        'help': 'Enable redflare in a channel.',
        'args': [
            {
                'name': 'enable?',
                'optional': False,
                'help': 'Enable or not.',
                },
            ]
        })
    return m


def enableredflare(fp, args):
    if not fp.channel:
        return 'You are not calling from a channel.'
    if fp.accesslevel() < 25:
        return 'You must be at least level 25.'
    try:
        fp.server.db[
            'redflare.enable.%s' % fp.channel.entry['channel']] = utils.boolstr(
                args.getlinstr('enable?'))
        return 'Enabled: ' + str(
            fp.server.db['redflare.enable.%s' % fp.channel.entry['channel']])
    except ValueError as e:
        return str(e)


def doredflare(fp, args):
    rf = redflare.RedFlare(args.getlinstr('url'))
    if 'stats' in args.lin:
        totalservers = len(rf.servers)
        totalplayers = 0
        for server in rf.servers:
            totalplayers += len(server['players'])
        return "Servers: %d, Players: %d" % (totalservers, totalplayers)
    else:
        search = args.getlinstr('search', '')
        endresults = []
        for server in rf.servers:
            results = []
            for player in server['players']:
                if configs.match.matchnocase(player, search, False):
                    results.append(player)
            if results:
                desc = server['description']
                endresults.append(desc + ': ' + ', '.join(results))
        rfes = 'redflare.enable.%s' % fp.channel.entry['channel']
        if fp.channel and rfes not in fp.server.db or not fp.server.db[rfes]:
            return 'Redflare is not enabled here.'
        if not endresults:
            return 'No results.'
        return '\n'.join(endresults)
