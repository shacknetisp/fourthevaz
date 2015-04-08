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
import datetime


def init(options):
    if 'redflares' not in options['server'].db:
        options['server'].db['redflares'] = {}

    options['server'].state['redflare'] = db.text.DB(
        configs.locs.userdata + '/redflare.py')
    if os.path.exists(configs.locs.userdata + '/redflare.py'):
        options['server'].state['redflare'].load()
    if 'list' not in options['server'].state['redflare'].db():
        options['server'].state['redflare'].db()['list'] = []
    options['server'].state['redflare'].save()

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
                'name': 'noservers',
                'keyvalue': '',
                'optional': True,
                'help': 'Show only players.',
                },
            {
                'name': 'servers',
                'keyvalue': '',
                'optional': True,
                'help': 'Search servers.',
                },
            {
                'name': '{playerstats/serverstats}',
                'keyvalue': '',
                'optional': True,
                'help': 'Show activity statistics.',
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
        'level': 25,
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
    m.add_timer_hook(60 * 1000, timer)
    return m


def timer():
    dbf = db.text.DB(configs.locs.userdata + '/redflare.py')
    dbdh = dbf.db()
    for url in dbdh['list']:
        rf = redflare.RedFlare(url)
        if 'lastseen' not in dbdh:
            dbdh['lastseen'] = {}
        if 'ac.players' not in dbdh:
            dbdh['ac.players'] = {}
        if 'ac.servers' not in dbdh:
            dbdh['ac.servers'] = {}
        if url not in dbdh:
            dbdh[url] = {}
        dbd = dbdh[url]
        if 'lastseen' not in dbd:
            dbd['lastseen'] = {}
        for server in rf.servers:
            for player in server['players']:
                dbd['lastseen'][player] = {
                    'server': server['description'],
                    'name': player,
                    'time': utils.utcepoch(),
                    }
        #Players
        if 'ac.players' not in dbdh[url]:
            dbdh[url]['ac.players'] = {}
        dbd = dbdh[url]['ac.players']
        if 'list' not in dbd:
            dbd['list'] = {}
        highest = 0
        for server in rf.servers:
            for player in server['players']:
                if player not in dbd['list']:
                    dbd['list'][player] = 0
                dbd['list'][player] += 1
                highest = max(highest, dbd['list'][player])
        if highest > 60 * 24 * 8:
            tod = []
            for p in dbd['list']:
                dbd['list'][p] = dbd['list'][p] / 2
                if dbd['list'][p] < 60:
                    tod.append(p)
            for todi in tod:
                del dbd['list'][todi]
        #Servers
        if 'ac.servers' not in dbdh[url]:
            dbdh[url]['ac.servers'] = {}
        dbd = dbdh[url]['ac.servers']
        if 'list' not in dbd:
            dbd['list'] = {}
        highest = 0
        for server in rf.servers:
            if server['description'] not in dbd['list']:
                dbd['list'][server['description']] = 0
            dbd['list'][server['description']] += len(server['players'])
            highest = max(highest, dbd['list'][server['description']])
        if highest > (60 * 24 * 8) / 4:
            tod = []
            for p in dbd['list']:
                dbd['list'][p] = dbd['list'][p] / 2
                if dbd['list'][p] < 60:
                    tod.append(p)
            for todi in tod:
                del dbd['list'][todi]
    dbf.save()


def redflares(fp, args):
    db = fp.server.state['redflare'].db()['list']
    if 'add' in args.lin:
        url = args.getlinstr('url')
        if url in db:
            return 'That url is already registered.'
        try:
            requests.get(url)
        except:
            return 'Inaccessable URL.'
        db.append(url)
        fp.server.state['redflare'].save()
        return '%s is now registered.' % url
    elif 'remove' in args.lin:
        url = args.getlinstr('url')
        if url not in db:
            return 'That url is not registered.'
        del db[db.index(url)]
        fp.server.state['redflare'].save()
        return '%s is now unregistered.' % url
    else:
        return 'Redflares: ' + utils.ltos(db)


def enableredflare(fp, args):
    if not fp.channel:
        return 'You are not calling from a channel.'
    try:
        fp.server.db[
            'redflare.enable.%s' % fp.channel.entry['channel']] = utils.boolstr(
                args.getlinstr('enable?'))
        return 'Enabled: ' + str(
            fp.server.db['redflare.enable.%s' % fp.channel.entry['channel']])
    except ValueError as e:
        return str(e)


def doredflare(fp, args):
    url = args.getlinstr('url')
    rf = redflare.RedFlare(args.getlinstr('url'))
    try:
        lsdb = fp.server.state['redflare'].db()[
            'lastseen'][args.getlinstr('url')]
    except KeyError:
        lsdb = None
    if 'stats' in args.lin:
        totalservers = len(rf.servers)
        totalplayers = 0
        for server in rf.servers:
            totalplayers += len(server['players'])
        return "Servers: %d, Players: %d" % (totalservers, totalplayers)
    elif 'lastseen' in args.lin:
        search = args.getlinstr('search', '')
        if not lsdb:
            return 'This URL is not registered.'
        best = None
        for k in lsdb:
            if configs.match.matchnocase(k, search, False):
                if not best or lsdb[k]['time'] > best['time']:
                    best = lsdb[k]
        if not best:
            return 'I have never seen %s.' % search
        return '"%s" was last seen on "%s" at %s.' % (
            best['name'],
            best['server'],
            datetime.datetime.fromtimestamp(
                best['time']).strftime('%Y-%m-%d %H:%M:%S UTC')
            )
    elif 'playerstats' in args.lin:
        search = args.getlinstr('search', '')
        acdb = fp.server.state['redflare'].db()[url][
            'ac.players']['list']
        sorteddb = list(
            reversed(sorted(list(acdb.items()), key=lambda x: x[1])))
        if not sorteddb:
            return 'No stats recorded.'
        ret = []
        number = 1
        for player in sorteddb:
            if configs.match.matchnocase(player[0], search, False):
                if len(ret) < 4 or(len(ret) >= 4 and len(
                    utils.ltos(ret)) < 128):
                    ret.append("%s (%d:%.2f)" % (player[0], number,
                round(player[1] / sorteddb[0][1], 2)))
            number += 1
        return utils.ltos(ret)
    elif 'serverstats' in args.lin:
        search = args.getlinstr('search', '')
        acdb = fp.server.state['redflare'].db()[url][
            'ac.servers']['list']
        sorteddb = list(
            reversed(sorted(list(acdb.items()), key=lambda x: x[1])))
        if not sorteddb:
            return 'No stats recorded.'
        ret = []
        number = 1
        for player in sorteddb:
            if configs.match.matchnocase(player[0], search, False):
                if len(ret) < 4 or(len(ret) >= 4 and len(
                    utils.ltos(ret)) < 128):
                    ret.append("%s (%d:%.2f)" % (player[0], number,
                round(player[1] / sorteddb[0][1], 2)))
            number += 1
        return utils.ltos(ret)
    else:
        search = args.getlinstr('search', '')
        searchservers = ('servers' in args.lin)
        if 'noservers' in args.lin:
            results = []
            for server in rf.servers:
                for player in server['players']:
                    if configs.match.matchnocase(player, search, False):
                        results.append(player)
            if not results:
                return 'No results.'
            return utils.ltos(results)
        endresults = []
        for server in rf.servers:
            results = []
            if (configs.match.matchnocase(server['description'],
                search, False) or not searchservers):
                for player in server['players']:
                    if (configs.match.matchnocase(player, search, False) or
                    searchservers):
                        results.append(player)
                if results:
                    desc = server['description']
                    endresults.append(desc + ': ' + ', '.join(results))
        if fp.channel and len(endresults) > 1:
            rfes = 'redflare.enable.%s' % fp.channel.entry['channel']
            if rfes not in fp.server.db or not fp.server.db[rfes]:
                return 'Redflare is not enabled here.'
        if not endresults:
            return 'No results.'
        return '\n'.join(endresults)
