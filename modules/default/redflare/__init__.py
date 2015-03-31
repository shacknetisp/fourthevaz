# -*- coding: utf-8 -*-
import configs.module
import configs.match
from . import redflare
import importlib
importlib.reload(redflare)
import utils
import db.text
import configs.locs
import os
import requests


def init(options):
    if 'redflares' not in options['server'].db:
        options['server'].db['redflares'] = {}
    options['server'].state['redflares'] = db.text.DB(
        configs.locs.userdata + '/redflares.py', list())
    if os.path.exists(configs.locs.userdata + '/redflares.py'):
        options['server'].state['redflares'].load()
    options['server'].state['redflares'].save()
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
                'name': 'lastseen',
                'keyvalue': '',
                'optional': True,
                'help': 'Show last seen statistics.',
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
    m.add_command_hook('redflares', {
        'function': redflares,
        'help': 'Manage redflares to get statistics from.',
        'args': [
            {
                'name': 'add',
                'keyvalue': '',
                'optional': True,
                'help': 'Add a redflare.',
                },
            {
                'name': 'remove',
                'keyvalue': '',
                'optional': True,
                'help': 'Remove a redflare.',
                },
            {
                'name': 'url',
                'optional': False,
                'help': 'The url.',
                'end': True,
                },
            ]
        })
    return m


def redflares(fp, args):
    db = fp.server.state['redflares'].db()
    if 'add' in args.lin:
        url = args.getlinstr('url')
        if url in db:
            return 'That url is already registered.'
        try:
            requests.get(url)
        except:
            return 'Unaccessable URL.'
        db.append(url)
        fp.server.state['redflares'].save()
        return '%s is now registered.' % url
    elif 'remove' in args.lin:
        url = args.getlinstr('url')
        if url not in db:
            return 'That url is not registered.'
        del db[db.index(url)]
        fp.server.state['redflares'].save()
        return '%s is now unregistered.' % url
    else:
        return 'Redflares: ' + utils.ltos(db)


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
    elif 'lastseen' in args.lin:
        return '"%s" was last seen on "%s" at %s.'
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
